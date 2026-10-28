import tempfile
import unittest
from pathlib import Path
from database import initialize_database, add_expense, get_expenses, update_expense, delete_expense, validate_expense, set_monthly_budget, get_monthly_budget

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.db=Path(self.tmp.name)/"test.db"; initialize_database(self.db)
    def tearDown(self): self.tmp.cleanup()
    def test_init_and_crud(self):
        eid=add_expense("Lunch",120,"Food","2026-01-02","work",self.db)
        self.assertEqual(len(get_expenses(self.db)),1)
        self.assertTrue(update_expense(eid,"Dinner",240,"Food","2026-01-03","",self.db))
        self.assertEqual(get_expenses(self.db)[0]["title"],"Dinner")
        self.assertTrue(delete_expense(eid,self.db)); self.assertEqual(get_expenses(self.db),[])
    def test_validation(self):
        for args in [("",1,"Food","2026-01-01"),("x",0,"Food","2026-01-01"),("x",1,"Food","bad")]:
            with self.assertRaises(ValueError): validate_expense(*args)
    def test_budget_persistence(self):
        set_monthly_budget(1000,self.db); self.assertEqual(get_monthly_budget(self.db),1000)
