"""Testes unitários para core/capabilities.

Evidência-first: apenas capacidades presentes no catálogo auditado.
Testa: importação, status válido, evidence não vazio, internal_capability SEM commercial_models, get_capability.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.capabilities.catalog import get_catalog, get_capability, CapabilityType
from core.capabilities.domains import Domain


def test_catalog_loads():
    """O catálogo carrega com capacidades >=10."""
    catalog = get_catalog()
    assert len(catalog) >= 10
    print(f"✓ Catalog carregou {len(catalog)} capacidades")


def test_capability_status_valid():
    """Todos os status de Capability válidos."""
    catalog = get_catalog()
    valid_statuses = {"implemented", "partial"}
    for cap in catalog:
        assert cap.status.lower() in valid_statuses
        assert cap.status.lower() in {"implemented", "partial"}
    print("✓ Todos os status válidos")


def test_capability_confidence_match_status():
    """implemented → 0.9, partial → 0.6."""
    catalog = get_catalog()
    for cap in catalog:
        if cap.status.lower() == "implemented":
            assert cap.confidence == 0.9
        else:
            assert cap.confidence == 0.6
    print("✓ Confiança corresponde ao status")


def test_capability_evidence_nonempty():
    """Todas as capabilities têm evidence não vazio."""
    catalog = get_catalog()
    for cap in catalog:
        assert len(cap.evidence) > 0
        assert len(cap.evidence[0]) > 0
    print("✓ Evidences não vazias")


def test_internal_capability_no_commercial_models():
    """Capabilities com type internal_capability não têm commercial_models."""
    catalog = get_catalog()
    for cap in catalog:
        if cap.type.lower() == "internal_capability":
            assert len(cap.commercial_models) == 0
    print("✓ Internal capabilities sem commercial_models")


def test_get_capability_works():
    """get_capability retorna Capability."""
    catalog = get_catalog()
    for cap in catalog:
        found = get_capability(cap.id)
        assert found is not None
        assert found.id == cap.id
    print("✓ get_capability funciona")


def test_domain_enum_exists():
    """Enum de domínios carregado."""
    from core.capabilities.domains import Domain, ALL_DOMAINS, ALL_DOMAIN_LABELS
    assert len(ALL_DOMAINS) >= 10
    assert len(ALL_DOMAIN_LABELS) >= 10
    for d in ALL_DOMAINS:
        assert d.value is not None
        assert d.label is not None
    print("✓ Domínios carregados")


def test_capability_types():
    """Capability types válidos."""
    catalog = get_catalog()
    valid_types = {"product", "service", "platform", "vertical", "infrastructure", "internal_capability"}
    for cap in catalog:
        assert cap.type.lower() in valid_types
    print("✓ Types válidos")


def test_domain_integration():
    """Capability.domain pode ser resovido como Domain enum."""
    catalog = get_catalog()
    for cap in catalog:
        domain_str = cap.domain
        found = any(d.value == domain_str for d in Domain)
        assert found
    print("✓ Domínios integrados")


def test_type_mapping_integrity():
    """Capacities são do tipo correto (internal vs. external)."""
    catalog = get_catalog()
    internal = [c for c in catalog if c.type.lower() == "internal_capability"]
    external = [c for c in catalog if c.type.lower() != "internal_capability"]
    assert len(internal) >= 1
    assert len(external) >= 1
    for cap in internal:
        assert len(cap.commercial_models) == 0
    for cap in external:
        assert len(cap.commercial_models) >= 0
    print("✓ Integridade de types")


def test_catalog_excluded():
    """CATALOG_EXCLUDED existe e tem entradas (PLANNED/UNKNOWN/HISTORICAL)."""
    from core.capabilities.catalog import CATALOG_EXCLUDED
    assert len(CATALOG_EXCLUDED) >= 20
    for entry in CATALOG_EXCLUDED:
        assert len(entry) == 2
        assert entry[0]
        assert entry[1]
    print(f"✓ CATALOG_EXCLUDED com {len(CATALOG_EXCLUDED)} entradas")


if __name__ == "__main__":
    test_catalog_loads()
    test_capability_status_valid()
    test_capability_confidence_match_status()
    test_capability_evidence_nonempty()
    test_internal_capability_no_commercial_models()
    test_get_capability_works()
    test_domain_enum_exists()
    test_capability_types()
    test_domain_integration()
    test_type_mapping_integrity()
    test_catalog_excluded()
    print("\n✅ Todos os testes de capabilities passaram")
