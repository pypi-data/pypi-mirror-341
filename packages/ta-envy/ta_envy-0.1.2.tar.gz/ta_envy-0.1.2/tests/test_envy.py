from ta_envy import Env
import tempfile

def test_envy_loading():
    content = "DEBUG=true\nPORT=8080\nTAGS=dev,api,test"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    env = Env(required=["DEBUG", "PORT"], dotenv_path=tmp_path)

    assert env.get("DEBUG", type=bool) is True
    assert env.get("PORT", type=int) == 8080
    assert env.get("TAGS", type=list) == ["dev", "api", "test"]
