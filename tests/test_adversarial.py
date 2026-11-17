from scripts.eval.run_adversarial import run


def test_every_attack_is_caught():
    misses = [r["id"] for r in run() if not r["caught"]]
    assert misses == []
