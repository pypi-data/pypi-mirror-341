from pytest_funcnodes import nodetest, all_nodes_tested
import funcnodes_chemprop as fnmodule  # noqa
import pandas as pd
import os
import numpy as np


def test_all_nodes_tested(all_nodes):
    all_nodes_tested(all_nodes, fnmodule.NODE_SHELF, ignore=[])


@nodetest(fnmodule.ChempropNode)
async def test_chemprop_node():
    # Test the ChempropNode with a dummy input
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "mol.csv"))
    smiles_column = "smiles"
    target_columns = "lipo"

    node = fnmodule.ChempropNode()

    node["df"] < df
    node["smiles_column"] < smiles_column
    node["target_columns"] < target_columns
    node["max_epochs"] < 2

    await node

    outdf = node["out_df"].value
    assert isinstance(outdf, pd.DataFrame), "Output should be a DataFrame"

    assert len(outdf) == len(df), (
        "Output DataFrame should have the same length as input"
    )

    assert "chemprop_role" in outdf.columns, (
        "Output DataFrame should contain 'chemprop_role' column"
    )

    assert "chemprop_prediction_lipo" in outdf.columns, (
        "Output DataFrame should contain 'chemprop_prediction' column"
    )

    # assert "chemprop_prediction_lipo" is all flaot

    assert np.issubdtype(outdf["chemprop_prediction_lipo"].dtype, np.floating), (
        "chemprop_prediction_lipo should be of float type"
    )

    # assert no nan

    assert not outdf["chemprop_prediction_lipo"].isnull().any(), (
        "NaN values found in chemprop_prediction_lipo"
    )


@nodetest(
    [fnmodule.make_model, fnmodule.MakeDataNode, fnmodule.predict, fnmodule.TrainNode]
)
async def test_make_model_node():
    # Test the ChempropNode with a dummy input
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "mol.csv"))
    smiles_column = "smiles"
    target_columns = "lipo"

    datanode = fnmodule.MakeDataNode()
    datanode["df"] < df
    datanode["smiles_column"] < smiles_column
    datanode["target_columns"] < target_columns

    await datanode

    modelnode = fnmodule.make_model()
    modelnode["scaler"] > datanode["scaler"]

    await modelnode

    model = modelnode["model"].value
    assert isinstance(model, fnmodule.models.MPNN), "Output should be a MPNN model"

    trainnode = fnmodule.TrainNode()
    trainnode["model"] > modelnode["model"]
    trainnode["train_loader"] > datanode["train_loader"]
    trainnode["val_loader"] > datanode["val_loader"]
    trainnode["test_loader"] > datanode["test_loader"]

    trainnode["max_epochs"] < 2

    await trainnode

    prednode = fnmodule.predict()

    prednode["model"] > trainnode["trained_model"]
    prednode["smiles"] < "CCC"

    await prednode

    preds = prednode["preds"].value
    assert isinstance(preds, np.ndarray), "Output should be a numpy array"
    assert preds.shape == (1, 1), "Output should have shape (1,)"
