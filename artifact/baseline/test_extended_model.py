import unittest
import extended_model as m


class LifecycleTests(unittest.TestCase):
    def test_copy_budget_boundary(self):
        self.assertGreater(m.explore(4, 3, 3, 1)["unsafe_barrier_states"], 0)
        self.assertEqual(m.explore(5, 4, 4, 1)["unsafe_barrier_states"], 0)
        self.assertGreater(m.explore(5, 4, 4, 2)["unsafe_barrier_states"], 0)

    def test_persistent_slot_closure(self):
        out = m.capsule_attacks()
        self.assertEqual(out["fresh_bank_exposed_shares"], 0)
        self.assertEqual(out["old_secret_still_recovered_after_bank_replacement"], 42)

    def test_independent_refresh_view(self):
        self.assertEqual(m.refresh_linear_views()["exposure_set_pairs"], 121)

    def test_reconstruction_and_field_validation(self):
        for coeff in ((0, 0, 0), (7, 13, 29), (100, 99, 98)):
            for selected in m.combinations(range(1, 6), 4):
                points = [(x, m.polynomial(42, coeff, x)) for x in selected]
                self.assertEqual(m.reconstruct(points), 42)

    def test_two_fault_availability(self):
        self.assertTrue(all(not x["one_byzantine_withholds_plus_one_honest_offline"] for x in m.availability()))


if __name__ == "__main__":
    unittest.main()
