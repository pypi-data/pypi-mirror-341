from funcnodes_chemprop import functions as fn
import pandas as pd
import os
from chemprop import models
import pytest


@pytest.mark.asyncio
async def test_chemprop_workflow():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "mol.csv"))
    smiles_column = "smiles"
    target_columns = ["lipo"]

    (
        train_loader,
        val_loader,
        test_loader,
        scaler,
        train_indices,
        val_indices,
        test_indices,
    ) = await fn.make_data(
        df, smiles_column, target_columns, split=(0.8, 0.1, 0.1), in_new_thread=True
    )

    model = fn.make_model(scaler)
    inipreds = await fn.predict(model, df[smiles_column], in_new_thread=False)

    initerror = ((df[target_columns].values - inipreds) ** 2).mean() ** 0.5

    assert initerror > 1, "Initial RMSE should be greater than 1"

    assert isinstance(
        model,
        models.MPNN,
    )

    import time

    start_time = time.time()
    async for metrics in fn.train_in_subprocess(
        model, train_loader, val_loader, test_loader, max_epochs=20
    ):
        print("\n", time.time() - start_time)

    model, results = metrics
    preds = await fn.predict(model, df[smiles_column], in_new_thread=False)

    # rmse
    error = ((df[target_columns].values - preds) ** 2).mean() ** 0.5

    assert error < initerror, "RMSE should be less than initial RMSE"
