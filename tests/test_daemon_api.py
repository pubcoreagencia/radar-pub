"""Testes de daemon e API."""
import sys, os, tempfile, gc, shutil, threading, time, json, urllib.request
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.daemon import RadarDaemon
from core.api import RadarAPI, RadarHandler
from core.persistence import Database
from integrations.hermes.client import HermesClient
from integrations.pdl.client import PDLClient


def _make_db():
    tmpdir = tempfile.mkdtemp(prefix="radar_daemon_test_")
    db_path = os.path.join(tmpdir, "test_daemon.db")
    return db_path, tmpdir


def _cleanup_db(db_path, tmpdir):
    gc.collect()
    for _ in range(5):
        try:
            shutil.rmtree(tmpdir, ignore_errors=False)
            return
        except PermissionError:
            import time; time.sleep(0.1)
    shutil.rmtree(tmpdir, ignore_errors=True)


def test_daemon_init():
    db_path, tmp = _make_db()
    daemon = RadarDaemon(db_path=db_path)
    assert daemon is not None
    assert daemon.discovery_interval > 0
    daemon.db.close()
    _cleanup_db(db_path, tmp)
    print("✓ daemon_init")


def test_daemon_discovery_loop():
    db_path, tmp = _make_db()
    daemon = RadarDaemon(db_path=db_path)
    daemon._discovery_loop()
    leads = daemon.db.get_leads()
    assert len(leads) == 3
    daemon.db.close()
    _cleanup_db(db_path, tmp)
    print("✓ daemon_discovery_loop")


def test_daemon_research_loop():
    db_path, tmp = _make_db()
    daemon = RadarDaemon(db_path=db_path)
    daemon._discovery_loop()
    daemon._research_loop()
    leads = daemon.db.get_leads()
    assert len(leads) == 3
    daemon.db.close()
    _cleanup_db(db_path, tmp)
    print("✓ daemon_research_loop")


def test_daemon_qualification_loop():
    db_path, tmp = _make_db()
    daemon = RadarDaemon(db_path=db_path)
    daemon._discovery_loop()
    daemon._research_loop()
    daemon._qualification_loop()
    opps = daemon.db.get_opportunities()
    assert len(opps) == 3
    daemon.db.close()
    _cleanup_db(db_path, tmp)
    print("✓ daemon_qualification_loop")


def test_api_health():
    from http.server import HTTPServer
    db_path, tmp = _make_db()
    db = Database(db_path)
    api = RadarAPI(db=db)
    RadarHandler.api = api
    server = HTTPServer(("127.0.0.1", 0), RadarHandler)
    port = server.server_address[1]
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.2)
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as resp:
            data = json.loads(resp.read())
            assert data["status"] == "ok"
        print("✓ api_health")
    finally:
        server.shutdown()
        server_thread.join(timeout=2)
        db.close()
        _cleanup_db(db_path, tmp)


def test_api_discover():
    from http.server import HTTPServer
    db_path, tmp = _make_db()
    db = Database(db_path)
    api = RadarAPI(db=db)
    RadarHandler.api = api
    server = HTTPServer(("127.0.0.1", 0), RadarHandler)
    port = server.server_address[1]
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.2)
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/discover", timeout=2) as resp:
            data = json.loads(resp.read())
            assert isinstance(data, list)
            assert len(data) == 3
        print("✓ api_discover")
    finally:
        server.shutdown()
        server_thread.join(timeout=2)
        db.close()
        _cleanup_db(db_path, tmp)


def test_api_priority_leads():
    from http.server import HTTPServer
    db_path, tmp = _make_db()
    db = Database(db_path)
    api = RadarAPI(db=db)
    RadarHandler.api = api
    server = HTTPServer(("127.0.0.1", 0), RadarHandler)
    port = server.server_address[1]
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.2)
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/priority-leads?min_score=0.8", timeout=2) as resp:
            data = json.loads(resp.read())
            assert isinstance(data, list)
            assert len(data) > 0
        print("✓ api_priority_leads")
    finally:
        server.shutdown()
        server_thread.join(timeout=2)
        db.close()
        _cleanup_db(db_path, tmp)


def test_integrations_build():
    hermes = HermesClient("http://localhost:8080")
    pdl = PDLClient("http://localhost:8081")
    assert hermes is not None
    assert pdl is not None
    print("✓ integrations_build")


def test_integrations_no_config():
    hermes = HermesClient("http://localhost:9999")
    result = hermes.discover()
    assert result == []
    print("✓ integrations_no_config")


if __name__ == "__main__":
    test_daemon_init()
    test_daemon_discovery_loop()
    test_daemon_research_loop()
    test_daemon_qualification_loop()
    test_api_health()
    test_api_discover()
    test_api_priority_leads()
    test_integrations_build()
    test_integrations_no_config()
    print("\n✅ Todos os testes de daemon/API/integration passaram")