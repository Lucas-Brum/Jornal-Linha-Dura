# Jornal-Linha-Dura
Jornal escrito e revisado por IA generativa apartir de informações do mundo real



### Requisitos
Esse projeto foi criado com **python 3.12.10**

### Como usar
Crie uma venv com:    
```Python3 -m venv venv```    
Logo apois entre na sua venv usando o PowerShell:   
```.\nome_da_venv\Scripts\Activate.ps1```   
Ou se usa o bash:   
``` source nome_da_venv/bin/activate```   

Atualmente estamos usando a [The News API](https://www.thenewsapi.com/) como fonte da informação,   
então para usar crie uma conta [em registro do The News API](https://www.thenewsapi.com/register),    
Valide seu email e peguei seu token No  [dashboard do The News API](https://www.thenewsapi.com/account/dashboard)    

Com seu token em mãos, apenas cole ele em **secrets/secrets.txt**   

E já estará pronto para usar o script:    
```python app.py```

