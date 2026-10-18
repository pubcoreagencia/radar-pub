"""Testes do módulo de configuração central."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import CONFIG, ScoringConfig, RadarConfig, update_config


def test_default_weights():
    assert CONFIG.scoring.weights["seo"] == 0.20
    assert CONFIG.scoring.weights["website"] == 0.25
    assert CONFIG.scoring.weights["social"] == 0.15
    assert CONFIG.scoring.weights["tracking"] == 0.10
    assert CONFIG.scoring.weights["conversion"] == 0.15
    assert CONFIG.scoring.weights["commercial_potential"] == 0.15
    print("✓ Default weights")


def test_total_weight():
    total = sum(CONFIG.scoring.weights.values())
    assert abs(total - 1.0) < 0.001
    print(f"✓ Total weight = {total:.2f}")


def test_thresholds():
    assert CONFIG.scoring.threshold_high == 0.70
    assert CONFIG.scoring.threshold_medium == 0.45
    print("✓ Thresholds")


def test_get_weight():
    w = CONFIG.scoring.get_weight("seo")
    assert w == 0.20
    print("✓ get_weight")


if __name__ == "__main__":
    test_default_weights()
    test_total_weight()
    test_thresholds()
    test_get_weight()
    print("\n✅ Todos os testes de configuração passaram")