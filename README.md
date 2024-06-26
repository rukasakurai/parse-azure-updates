# このリポジトリについて
Azure UpdatesをCSVに出力します。

## 前提
 * Azure OpenAIサービスでアカウントが作られていること
 * Public AccessがAllowされていること(リソース管理>ネットワークから確認)
 * (Azure AD認証を行う場合)認証する主体がAzure OpenAIサービスアカウントに対してCognitive Services OpenAI Userロールを持っていること

### 作成されていない場合
```
az group create --name rg-parse-azure-updates --location japaneast

az bicep upgrade

az deployment group create --resource-group rg-parse-azure-updates --template-file ./infra/main.bicep
```

## 使い方

### パッケージのインストール
```bash
pip install -r requirements.txt
```
### 変数
```bash
export OPENAI_API_KEY="xxxxxxxxxxxxxxxxxxxx"
```
APIキーはポータルのAzure OpenAIアカウントの「リソース管理」 > 「キーとエンドポイント」から確認できます。

### エンドポイントの修正
```bash
export OPENAI_API_ENDPOINT="xxxxxxxxxxxxxxxxxxxx"
```
作成されたAzure OpenAIアカウントの概要 > エンドポイント

```bash
export OPENAI_ENGINE="xxxxxxxxxxxxxxxxxxxx"
```
Azure OpenAIアカウントのリソース管理 > モデル デプロイ から確認できるモデル デプロイ名

### 呼び出し

```bash
python main.py
```

or 

```bash
python main.py --context "I develop and maintain applications at Contoso. At Contoso, our applications currently mainly run on Azure App Service, and we mainly use Azure SQL for our databases. While we currently do not use Azure's AI services, we are interested in potentially leveraging them in the future."
```

### 既知バグ
- Azure UpdatesのHTMLをparseしているため、Azure UpdatesのUI更新があると、おそらく機能しなくなります
- Azure OpenAIに生成されるカテゴリに表記のバラツキがあります（例: `GA`, `General Availability`）

### 参考
https://github.com/openai/openai-python
