"""Chronological monthly expense prediction using scikit-learn LinearRegression."""
from dataclasses import dataclass
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from analytics import monthly_totals

@dataclass
class PredictionResult:
    ready: bool
    message: str
    history: pd.Series
    next_month: pd.Timestamp | None = None
    prediction: float | None = None
    mae: float | None = None
    model_name: str = "Linear Regression"

def predict_next_month(expenses, minimum_months=6, evaluate=True):
    history=monthly_totals(expenses,fill_gaps=True)
    if len(history)<minimum_months:
        return PredictionResult(False, f"At least {minimum_months} calendar months of recorded history are needed; found {len(history)}. Add more dated expenses and try again.", history)
    # Time index is the only feature; split chronologically before fitting the holdout model.
    x=pd.DataFrame({"month_index":range(len(history))})
    y=history.to_numpy(dtype=float)
    mae=None
    if evaluate and len(history)>=8:
        split=max(3,int(len(history)*0.8))
        if len(history)-split>=1:
            holdout=LinearRegression().fit(x.iloc[:split],y[:split])
            mae=float(mean_absolute_error(y[split:],holdout.predict(x.iloc[split:])))
    model=LinearRegression().fit(x,y)
    prediction=max(0.0,float(model.predict(pd.DataFrame({"month_index":[len(history)]}))[0]))
    next_month=history.index[-1]+pd.offsets.MonthBegin(1)
    return PredictionResult(True,"Prediction uses the chronological monthly totals recorded in your database.",history,next_month,prediction,mae)
