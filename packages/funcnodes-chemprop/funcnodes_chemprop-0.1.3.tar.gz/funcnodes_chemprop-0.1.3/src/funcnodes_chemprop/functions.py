import pandas as pd
from typing import List, Tuple, Union, Optional
from chemprop import data, featurizers, models, nn
from lightning import pytorch as pl
from sklearn.preprocessing import StandardScaler
import torch
from torch.utils.data import DataLoader
import numpy as np
import multiprocessing
from tqdm import tqdm
import asyncio
from funcnodes_core.utils.functions import make_run_in_new_process


def make_model(scaler: StandardScaler) -> models.MPNN:
    mp = nn.BondMessagePassing()

    agg = nn.MeanAggregation()

    output_transform = nn.UnscaleTransform.from_standard_scaler(scaler)
    predictor = nn.RegressionFFN(output_transform=output_transform)
    batch_norm = True
    metric_list = [
        nn.metrics.RMSE(),
        nn.metrics.MAE(),
    ]  # Only the first metric is used for training and early stopping
    mpnn = models.MPNN(
        mp, agg, predictor=predictor, batch_norm=batch_norm, metrics=metric_list
    )
    return mpnn


def model_to_scaler(model: models.MPNN) -> StandardScaler:
    scaler = model.predictor.output_transform.to_standard_scaler()
    return scaler


async def make_data(
    df: pd.DataFrame,
    smiles_column: str,
    target_columns: Union[str, List[str]],
    split=(0.8, 0.1, 0.1),
    scaler: StandardScaler = None,
    split_type="random",
    progess_bar: Optional[tqdm] = None,
    in_new_thread: bool = True,
) -> Tuple[
    DataLoader,
    DataLoader,
    DataLoader,
    StandardScaler,
]:
    def _make_data(
        df, smiles_column, target_columns, split, scaler, split_type, progess_bar
    ):
        num_workers = 0
        if isinstance(target_columns, str):
            target_columns = [target_columns]
        if progess_bar is not None:
            progess_bar.set_description("Loading data")
            # set the total number of iterations to 3
            progess_bar.total = 4
            progess_bar.n = 0
            progess_bar.refresh()
        smis = df.loc[:, smiles_column].values
        ys = df.loc[:, target_columns].values
        all_data = [data.MoleculeDatapoint.from_smi(smi, y) for smi, y in zip(smis, ys)]
        if progess_bar is not None:
            progess_bar.update(1)
        mols = [
            d.mol for d in all_data
        ]  # RDkit Mol objects are use for structure based splits
        train_indices, val_indices, test_indices = data.make_split_indices(
            mols, split_type, split
        )
        train_data, val_data, test_data = data.split_data_by_indices(
            all_data, train_indices, val_indices, test_indices
        )
        if progess_bar is not None:
            progess_bar.update(1)
        featurizer = featurizers.SimpleMoleculeMolGraphFeaturizer()
        train_dset = data.MoleculeDataset(train_data[0], featurizer)
        scaler = train_dset.normalize_targets(scaler)

        val_dset = data.MoleculeDataset(val_data[0], featurizer)
        val_dset.normalize_targets(scaler)

        test_dset = data.MoleculeDataset(test_data[0], featurizer)

        if progess_bar is not None:
            progess_bar.update(1)

        train_loader = data.build_dataloader(train_dset, num_workers=num_workers)

        val_loader = data.build_dataloader(
            val_dset, num_workers=num_workers, shuffle=False
        )
        test_loader = data.build_dataloader(
            test_dset, num_workers=num_workers, shuffle=False
        )
        if progess_bar is not None:
            progess_bar.update(1)

        return (
            train_loader,
            val_loader,
            test_loader,
            scaler,
            train_indices[0],
            val_indices[0],
            test_indices[0],
        )

    if in_new_thread:
        # Offload the blocking _make_data function to a separate thread.
        return await asyncio.to_thread(
            _make_data,
            df,
            smiles_column,
            target_columns,
            split,
            scaler,
            split_type,
            progess_bar,
        )
    else:
        # Run _make_data directly in the current coroutine.
        return _make_data(
            df, smiles_column, target_columns, split, scaler, split_type, progess_bar
        )


class MetricCallback(pl.Callback):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def log_metrics2queue(self, trainer):
        metrics = trainer.callback_metrics
        # convert tensors to scalars
        metrics = {k: v.item() for k, v in metrics.items()}
        metrics["epoch"] = trainer.current_epoch
        self.queue.put(metrics)

    def on_train_epoch_end(
        self,
        trainer,
        pl_module,
    ):
        self.log_metrics2queue(trainer)

    def on_test_epoch_end(
        self, trainer: pl.Trainer, pl_module: pl.LightningModule
    ) -> None:
        self.log_metrics2queue(trainer)


def train(
    model: models.MPNN,
    train_loader: DataLoader,
    val_loader: DataLoader,
    test_loader: DataLoader,
    max_epochs=20,
    queue=None,
) -> Tuple[models.MPNN, dict]:
    callbacks = [MetricCallback(queue)] if queue else []
    trainer = pl.Trainer(
        logger=False,
        enable_progress_bar=True,
        accelerator="auto",
        max_epochs=max_epochs,  # number of epochs to train for
        callbacks=callbacks,
        enable_checkpointing=False,
        enable_model_summary=False,
    )

    trainer.fit(model, train_loader, val_loader)

    results = trainer.test(model, test_loader)
    return model, results


def _train_in_subprocess_entry(
    model,
    train_loader,
    val_loader,
    test_loader,
    max_epochs,
    return_dict,
    queue: multiprocessing.Queue,
):
    model, results = train(
        model,
        train_loader,
        val_loader,
        test_loader,
        max_epochs,
        queue,
    )
    return_dict["model"] = model
    return_dict["results"] = results
    return return_dict


_train_in_subprocess = make_run_in_new_process(_train_in_subprocess_entry)


async def train_in_subprocess(
    model: models.MPNN,
    train_loader: DataLoader,
    val_loader: DataLoader,
    test_loader: DataLoader,
    max_epochs=20,
) -> Tuple[models.MPNN, dict]:
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    queue = manager.Queue()

    # p = multiprocessing.Process(
    #     target=_train_in_subprocess_entry,
    #     args=(
    #         model,
    #         train_loader,
    #         val_loader,
    #         test_loader,
    #         max_epochs,
    #         return_dict,
    #         queue,
    #     ),
    # )
    # p.start()

    async def _runner():
        # Run the training in a new process
        return await _train_in_subprocess(
            model,
            train_loader,
            val_loader,
            test_loader,
            max_epochs,
            return_dict,
            queue,
        )

    task = asyncio.create_task(_runner())

    async def metric_generator(queue):
        # while p.is_alive():
        while not task.done():
            # Check if there are metrics in the queue
            try:
                metrics = queue.get_nowait()
                yield metrics
            except Exception:
                await asyncio.sleep(0.1)

    metrics_generator = metric_generator(queue)
    async for metrics in metrics_generator:
        yield metrics
    # p.join()

    yield return_dict["model"], return_dict["results"]


async def predict(
    model: models.MPNN,
    smis: List[str],
    in_new_thread: bool = True,
) -> np.ndarray:
    def _pred(model, smis):
        test_data = [data.MoleculeDatapoint.from_smi(smi) for smi in smis]
        featurizer = featurizers.SimpleMoleculeMolGraphFeaturizer()
        test_dset = data.MoleculeDataset(test_data, featurizer=featurizer)
        test_loader = data.build_dataloader(test_dset, shuffle=False)
        with torch.inference_mode():
            trainer = pl.Trainer(
                logger=False,
                enable_progress_bar=True,
                accelerator="auto",
                enable_checkpointing=False,
                enable_model_summary=False,
            )
            test_preds = trainer.predict(model, test_loader)
        test_preds = np.concatenate(test_preds, axis=0)

        return test_preds

    if in_new_thread:
        # Offload the blocking _pred function to a separate thread.
        return await asyncio.to_thread(_pred, model, smis)
    else:
        # Run _pred directly in the current coroutine.
        return _pred(model, smis)
