## import error
sys.path
['C:\\Users\\vetrivel\\src\\GitHub\\hpe-opsramp-cli\\tests', 'C:\\Users\\vetrivel\\AppData\\Local\\uv\\cache\\archive-v0\\nGHnLQzK3ShbxL9VaUxxf\\Scripts\\pytest.exe', 'C:\\Users\\vetrivel\\scoop\\apps\\python\\current\\python312.zip', 'C:\\Users\\vetrivel\\scoop\\apps\\python\\current\\DLLs', 'C:\\Users\\vetrivel\\scoop\\apps\\python\\current\\Lib', 'C:\\Users\\vetrivel\\scoop\\apps\\python\\current', 'C:\\Users\\vetrivel\\AppData\\Local\\uv\\cache\\archive-v0\\nGHnLQzK3ShbxL9VaUxxf', 'C:\\Users\\vetrivel\\AppData\\Local\\uv\\cache\\archive-v0\\nGHnLQzK3ShbxL9VaUxxf\\Lib\\site-packages', WindowsPath('C:/Users/vetrivel/src/GitHub/hpe-opsramp-cli'), 'C:\\Users\\vetrivel\\src\\GitHub\\hpe-opsramp-cli\\src']

C:\Users\vetrivel\src\GitHub\hpe-opsramp-cli\src\hpe_opsramp_cli
C:\\Users\\vetrivel\\src\\GitHub\\hpe-opsramp-cli\\src
C:\Users\vetrivel\src\GitHub\hpe-opsramp-cli\src

(hpe-opsramp-cli) PS C:\Users\vetrivel\src\GitHub\hpe-opsramp-cli> uvx pytest
====================================================================== test session starts =======================================================================
platform win32 -- Python 3.12.6, pytest-8.3.5, pluggy-1.5.0
rootdir: C:\Users\vetrivel\src\GitHub\hpe-opsramp-cli
configfile: pyproject.toml
collected 0 items / 2 errors

============================================================================= ERRORS =============================================================================
____________________________________________ ERROR collecting tests/hpe_opsramp_cli_test/test_opsramp_environment.py _____________________________________________ 
ImportError while importing test module 'C:\Users\vetrivel\src\GitHub\hpe-opsramp-cli\tests\hpe_opsramp_cli_test\test_opsramp_environment.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests\hpe_opsramp_cli_test\test_opsramp_environment.py:8: in <module>
    from hpe_opsramp_cli.opsramp_environment import OpsRampEnvironment
E   ModuleNotFoundError: No module named 'hpe_opsramp_cli'

During handling of the above exception, another exception occurred:
..\..\..\scoop\apps\python\current\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests\hpe_opsramp_cli_test\test_opsramp_environment.py:16: in <module>
    from src.hpe_opsramp_cli.opsramp_environment import OpsRampEnvironment
E   ModuleNotFoundError: No module named 'src'
__________________________________________ ERROR collecting tests/hpe_opsramp_cli_test/test_unmanage_alert_resources.py __________________________________________ 
ImportError while importing test module 'C:\Users\vetrivel\src\GitHub\hpe-opsramp-cli\tests\hpe_opsramp_cli_test\test_unmanage_alert_resources.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\scoop\apps\python\current\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests\hpe_opsramp_cli_test\test_unmanage_alert_resources.py:3: in <module>
    from typer.testing import CliRunner
E   ModuleNotFoundError: No module named 'typer'
==================================================================== short test summary info ===================================================================== 
ERROR tests/hpe_opsramp_cli_test/test_opsramp_environment.py
ERROR tests/hpe_opsramp_cli_test/test_unmanage_alert_resources.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
======================================================================= 2 errors in 0.16s ======================================================================== 
(hpe-opsramp-cli) PS C:\Users\vetrivel\src\GitHub\hpe-opsramp-cli> 