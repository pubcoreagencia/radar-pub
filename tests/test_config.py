"""Testes do módulo de configuração central."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import CONFIG, ScoringConfig, RadarConfig, update_config


def test_default_weights():
    assert CONFIG.scoring.weights["seo"] == 0.12
    assert CONFIG.scoring.weights["website"] == 0.15
    assert CONFIG.scoring.weights["social"] == 0.10
    assert CONFIG.scoring.weights["tracking"] == 0.08
    assert CONFIG.scoring.weights["conversion"] == 0.10
    assert CONFIG.scoring.weights["commercial_potential"] == 0.10
    assert CONFIG.scoring.weights["capability_fit"] == 0.15
    assert CONFIG.scoring.weights["commercial_fit"] == 0.12
    assert CONFIG.scoring.weights["confidence"] == 0.08
    print("✓ Default weights (9 dimensões)")


def test_total_weight():
    total = sum(CONFIG.scoring.weights.values())
    assert abs(total - 1.0) < 0.001
    print(f"✓ Total weight = {total:.2f}")


def test_thresholds():
    assert CONFIG.scoring.threshold_high == 0.70
    assert CONFIG.scoring.threshold_medium == 0.45
    assert CONFIG.scoring.threshold_low == 0.25
    print("✓ Thresholds")


def test_get_weight():
    w = CONFIG.scoring.get_weight("seo")
    assert w == 0.12
    print("✓ get_weight")


if __name__ == "__main__":
    test_default_weights()
    test_total_weight()
    test_thresholds()
    test_get_weight()
    print("\n✅ Todos os testes de config passaram")