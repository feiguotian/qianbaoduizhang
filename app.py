import streamlit as st
import pandas as pd
import requests

# 获取钱包交易数据
def get_wallet_transactions(wallet_address):
    url = "https://api.helius.xyz/v0/transactions"
    params = {
        "api-key": "your-helius-api-key",  # 替换为你的Helius API密钥
        "address": wallet_address,
        "limit": 100
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("无法获取交易数据。")
        return []

# 筛选与WSOL相关的交易
def filter_wsol_transactions(transactions):
    wsol_transactions = []
    
    for tx in transactions:
        if "WSOL" in [instruction.get("token") for instruction in tx.get("instructions", [])]:
            wsol_transactions.append(tx)
    
    return wsol_transactions

# 提取交易信息
def extract_transaction_details(transactions):
    details = []
    for tx in transactions:
        for instruction in tx.get("instructions", []):
            if "WSOL" in instruction.get("token"):
                details.append({
                    "交易类型": instruction.get("type", "未知"),
                    "币种": "SOL",
                    "余额": instruction.get("preBalances", [0])[-1]  # 余额变化
                })
    return details

# 展示表格
def display_transactions_table(wallet_address):
    transactions = get_wallet_transactions(wallet_address)
    wsol_transactions = filter_wsol_transactions(transactions)
    details = extract_transaction_details(wsol_transactions)

    if details:
        df = pd.DataFrame(details)
        st.write(df)
        
        # CSV 导出功能
        st.download_button(
            label="导出CSV",
            data=df.to_csv(index=False),
            file_name=f"{wallet_address}_transactions.csv",
            mime="text/csv"
        )
    else:
        st.write("未找到与WSOL相关的交易。")

# Streamlit界面
st.title("Solana 钱包交易流水查询")

wallet_address = st.text_input("请输入Solana钱包地址")
if wallet_address:
    display_transactions_table(wallet_address)
