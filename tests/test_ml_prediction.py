import unittest
from analytics import monthly_totals
from ml_prediction import predict_next_month

class PredictionTests(unittest.TestCase):
    def test_monthly_aggregation_fills_gaps_with_zero(self):
        rows=[{"amount":10,"expense_date":"2026-01-03"},{"amount":5,"expense_date":"2026-03-04"},{"amount":8,"expense_date":"bad"}]
        values=monthly_totals(rows)
        self.assertEqual(list(values),[10,0,5])
    def test_insufficient_and_invalid(self):
        result=predict_next_month([{"amount":1,"expense_date":"bad"}])
        self.assertFalse(result.ready); self.assertIsNone(result.prediction)
    def test_prediction_with_sufficient_history(self):
        rows=[]
        for m in range(1,10): rows.append({"amount":100+m*10,"expense_date":f"2026-{m:02d}-10"})
        result=predict_next_month(rows)
        self.assertTrue(result.ready); self.assertGreater(result.prediction,0); self.assertIsNotNone(result.mae)
