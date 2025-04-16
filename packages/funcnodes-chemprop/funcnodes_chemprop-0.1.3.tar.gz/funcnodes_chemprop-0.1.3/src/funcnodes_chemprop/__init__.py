import pandas as pd
from typing import List, Tuple, Union
from chemprop import models
from chemprop.data import SplitType
from sklearn.preprocessing import StandardScaler

from torch.utils.data import DataLoader
import numpy as np
import funcnodes as fn
from . import functions as f
import copy
import asyncio


@fn.NodeDecorator(
    id="chemprop.make_model",
    name="Make Model",
    description="Create a Chemprop model",
    outputs=[{"name": "model"}],
)
def make_model(scaler: StandardScaler) -> models.MPNN:
    mpnn = f.make_model(scaler)
    return mpnn


class MakeDataNode(fn.Node):
    node_id = "chemprop.make_data"
    node_name = "Make Data"
    description = "Create Chemprop data loaders"

    df = fn.NodeInput(uuid="df", type=pd.DataFrame)
    smiles_column = fn.NodeInput(uuid="smiles_column", type=str)
    target_columns = fn.NodeInput(uuid="target_columns", type=str)
    split = fn.NodeInput(
        uuid="split", type=Tuple[float, float, float], default=(0.8, 0.1, 0.1)
    )

    train_loader = fn.NodeOutput(uuid="train_loader", type=DataLoader)
    val_loader = fn.NodeOutput(uuid="val_loader", type=DataLoader)
    test_loader = fn.NodeOutput(uuid="test_loader", type=DataLoader)
    scaler = fn.NodeOutput(uuid="scaler", type=StandardScaler)

    def __init__(self):
        super().__init__()
        self.get_input("df").on("after_set_value", self._update_columns)

    def _update_columns(self, **kwargs):
        try:
            df = self.get_input("df").value
            smiles_column = self.get_input("smiles_column")
            target_columns = self.get_input("target_columns")
        except KeyError:
            return
        try:
            smiles_column.update_value_options(options=list(df.columns))
            target_columns.update_value_options(options=list(df.columns))
        except Exception:
            smiles_column.update_value_options(options=[])
            target_columns.update_value_options(options=[])

    async def func(self, df, smiles_column, target_columns, split):
        (
            train_loader,
            val_loader,
            test_loader,
            scaler,
            train_indices,
            val_indices,
            test_indices,
        ) = await f.make_data(df, smiles_column, target_columns, split)

        self.outputs["train_loader"].value = train_loader
        self.outputs["val_loader"].value = val_loader
        self.outputs["test_loader"].value = test_loader
        self.outputs["scaler"].value = scaler


# @fn.NodeDecorator(
#     id="chemprop.train",
#     name="Train",
#     description="Train a Chemprop model",
#     outputs=[{"name": "trained model"}, {"name": "results"}],
#     default_io_options={
#         "model": {"does_trigger": False},
#         "train_loader": {"does_trigger": False},
#         "val_loader": {"does_trigger": False},
#         "test_loader": {"does_trigger": False},
#         "max_epochs": {"does_trigger": False},
#     },
# )
# async def train(
#     model: models.MPNN,
#     train_loader: DataLoader,
#     val_loader: DataLoader,
#     test_loader: DataLoader,
#     max_epochs: int = 20,
# ) -> Tuple[models.MPNN, dict, pd.DataFrame]:
#     model_copy = copy.deepcopy(model)
#     metrics_df = None

#     async for metrics in f.train_in_subprocess(
#         model_copy, train_loader, val_loader, test_loader, max_epochs
#     ):
#         if isinstance(metrics, dict):
#             if metrics_df is None:
#                 metrics_df = pd.DataFrame([metrics])
#             else:
#                 metrics_df = pd.concat([metrics_df, pd.DataFrame([metrics])])
#         print(f"Received metrics: {metrics}")

#     return (*metrics, metrics_df)


class TrainNode(fn.Node):
    node_id = "chemprop.train"
    node_name = "Train"
    description = "Train a Chemprop model"

    model = fn.NodeInput(uuid="model", type=models.MPNN, does_trigger=False)

    train_loader = fn.NodeInput(
        uuid="train_loader", type=DataLoader, does_trigger=False
    )
    val_loader = fn.NodeInput(uuid="val_loader", type=DataLoader, does_trigger=False)
    test_loader = fn.NodeInput(uuid="test_loader", type=DataLoader, does_trigger=False)
    max_epochs = fn.NodeInput(
        uuid="max_epochs", type=int, default=20, does_trigger=False
    )

    trained_model = fn.NodeOutput(uuid="trained_model", type=models.MPNN)
    results = fn.NodeOutput(uuid="results", type=dict)
    metrics = fn.NodeOutput(uuid="metrics", type=pd.DataFrame)

    async def func(self, model, train_loader, val_loader, test_loader, max_epochs):
        model_copy = copy.deepcopy(model)

        metrics_df = None
        collected_metrics = []
        running = True

        async def metrics_publisher():
            last_published = 0
            while running:
                if len(collected_metrics) > last_published:
                    self.outputs["metrics"].value = pd.DataFrame(collected_metrics)
                    last_published = len(collected_metrics)
                await asyncio.sleep(1)

        publish_task = asyncio.create_task(metrics_publisher())

        with self.progress(
            desc="Training",
            total=max_epochs,
            unit="epoch",
            initial=0,
        ) as progress:
            async for metrics in f.train_in_subprocess(
                model_copy, train_loader, val_loader, test_loader, max_epochs
            ):
                if isinstance(metrics, dict):
                    ep = metrics["epoch"]
                    progress.update(int(ep - progress.n))
                    del metrics["epoch"]
                    converted_metrics = [
                        {"epoch": ep, "type": k, "value": v} for k, v in metrics.items()
                    ]
                    collected_metrics.extend(converted_metrics)

            running = False
            await publish_task
            # publish_thread.join()
        trained_model, results = metrics
        self.outputs["trained_model"].value = trained_model
        self.outputs["results"].value = results

        return trained_model, results, metrics_df


class ChempropNode(fn.Node):
    node_id = "chemprop.chemprop"
    node_name = "Chemprop"
    description = "Chemprop Node"

    model = fn.NodeInput(
        uuid="model", type=models.MPNN, does_trigger=False, default=None
    )
    df = fn.NodeInput(uuid="df", type=pd.DataFrame, does_trigger=False)
    smiles_column = fn.NodeInput(uuid="smiles_column", type=str, does_trigger=False)
    target_columns = fn.NodeInput(uuid="target_columns", type=str, does_trigger=False)
    split = fn.NodeInput(
        uuid="split",
        type=Tuple[float, float, float],
        default=(0.8, 0.1, 0.1),
        does_trigger=False,
        hidden=True,
    )
    split_type = fn.NodeInput(
        uuid="split_type",
        type=str,
        default="random",
        value_options={"options": [v.lower() for v in SplitType.values()]},
        does_trigger=False,
        hidden=True,
    )
    max_epochs = fn.NodeInput(
        uuid="max_epochs",
        type=int,
        default=20,
        does_trigger=False,
    )

    trained_model = fn.NodeOutput(uuid="trained_model", type=models.MPNN)
    results = fn.NodeOutput(uuid="results", type=dict)
    metrics = fn.NodeOutput(uuid="metrics", type=pd.DataFrame)
    out_df = fn.NodeOutput(uuid="out_df", type=pd.DataFrame)

    def __init__(self):
        super().__init__()
        self.get_input("df").on("after_set_value", self._update_columns)

    def _update_columns(self, **kwargs):
        try:
            df = self.get_input("df").value
            smiles_column = self.get_input("smiles_column")
            target_columns = self.get_input("target_columns")
        except KeyError:
            return
        try:
            smiles_column.update_value_options(options=list(df.columns))
            target_columns.update_value_options(options=list(df.columns))
        except Exception:
            smiles_column.update_value_options(options=[])
            target_columns.update_value_options(options=[])

    async def func(
        self,
        df,
        smiles_column,
        target_columns,
        model=None,
        max_epochs=20,
        split=(0.8, 0.1, 0.1),
        split_type="random",
    ):
        if isinstance(target_columns, str):
            target_columns = [target_columns]

        with self.progress(
            desc="Make Data",
        ) as progress:
            (
                train_loader,
                val_loader,
                test_loader,
                scaler,
                train_indices,
                val_indices,
                test_indices,
            ) = await f.make_data(
                df,
                smiles_column,
                target_columns,
                split,
                scaler=f.model_to_scaler(model) if model else None,
                split_type=split_type,
            )

        if model is None:
            model_copy = f.make_model(scaler)
        else:
            model_copy = copy.deepcopy(model)

        metrics_df = None
        collected_metrics = []
        running = True

        async def metrics_publisher():
            last_published = 0
            while running:
                if len(collected_metrics) > last_published:
                    self.outputs["metrics"].value = pd.DataFrame(collected_metrics)
                    last_published = len(collected_metrics)
                await asyncio.sleep(1)

        publish_task = asyncio.create_task(metrics_publisher())

        with self.progress(
            desc="Training",
            total=max_epochs,
            unit="epoch",
            initial=0,
        ) as progress:
            async for metrics in f.train_in_subprocess(
                model_copy, train_loader, val_loader, test_loader, max_epochs
            ):
                if isinstance(metrics, dict):
                    ep = metrics["epoch"]
                    progress.update(int(ep - progress.n))
                    del metrics["epoch"]
                    converted_metrics = [
                        {"epoch": ep, "type": k, "value": v} for k, v in metrics.items()
                    ]
                    collected_metrics.extend(converted_metrics)

            running = False
            await publish_task
            # publish_thread.join()
        trained_model, results = metrics

        out_df = df.copy()
        out_df["chemprop_role"] = "train"
        out_df.loc[train_indices, "chemprop_role"] = "train"
        out_df.loc[val_indices, "chemprop_role"] = "val"
        out_df.loc[test_indices, "chemprop_role"] = "test"
        preds = await f.predict(trained_model, df[smiles_column])
        out_df[["chemprop_prediction_" + s for s in target_columns]] = preds
        self.outputs["results"].value = results
        self.outputs["out_df"].value = out_df
        self.outputs["trained_model"].value = trained_model
        return trained_model, results, metrics_df, out_df


@fn.NodeDecorator(
    id="chemprop.predict",
    name="Predict",
    description="Predict using a Chemprop model",
    outputs=[{"name": "preds"}],
)
async def predict(model: models.MPNN, smiles: Union[str, List[str]]) -> np.ndarray:
    if isinstance(smiles, str):
        smiles = [smiles]
    return await f.predict(model, smiles)


NODE_SHELF = fn.Shelf(
    name="Chemprop",
    description="Chemprop nodes",
    nodes=[ChempropNode, make_model, MakeDataNode, TrainNode, predict],
    subshelves=[],
)
