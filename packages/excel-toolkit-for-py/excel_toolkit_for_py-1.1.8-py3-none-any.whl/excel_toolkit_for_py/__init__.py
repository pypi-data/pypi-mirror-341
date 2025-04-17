"""
Excel Toolkit for Python - Um conjunto de ferramentas para manipulação de arquivos Excel
"""

from .reader import read_excel, read_csv, get_sheet_names, get_dict_sheets
from .writer import write_excel, write_csv, write_list_to_excel
from .conversions import excel_to_json, json_to_excel
from .validations import validate_excel_schema
from .advanced_features import (
    read_protected_excel,
    validate_empty_cells,
    apply_conditional_formatting,
    extract_formulas,
    add_chart,
    protect_excel
)

__version__ = "1.1.7"
__author__ = "Roberto Lima"
__email__ = "robertolima.izphera@gmail.com"

__all__ = [
    # Funções básicas
    'read_excel',
    'read_csv',
    'get_sheet_names',
    'get_dict_sheets',
    'write_excel',
    'write_csv',
    'write_list_to_excel',
    'excel_to_json',
    'json_to_excel',
    'validate_excel_schema',
    
    # Funções avançadas
    'read_protected_excel',
    'validate_empty_cells',
    'apply_conditional_formatting',
    'extract_formulas',
    'add_chart',
    'protect_excel'
]
