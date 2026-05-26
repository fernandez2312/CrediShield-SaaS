def mask_cnpj(cnpj: str) -> str:
    """
    Recebe um CNPJ limpo (14 dígitos) e retorna formatado e mascarado.
    Exemplo: '12345678000199' -> '12.***.***/0001-99'
    """
    # Remove caracteres extras por segurança
    clean_cnpj = "".join(filter(str.isdigit, cnpj))
    
    if len(clean_cnpj) != 14:
        return "CNPJ_INVALIDO"
        
    return f"{clean_cnpj[:2]}.***.***/{clean_cnpj[8:12]}-{clean_cnpj[12:]}"
