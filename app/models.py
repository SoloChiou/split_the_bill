from . import db
from datetime import datetime
from sqlalchemy import CheckConstraint, Table

# 定義多對多關係表
expense_in_user = Table('expense_in_user', db.Model.metadata,
    db.Column('expense_id', db.Integer, db.ForeignKey('expense.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

def create_group_id_column():
    return db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    currency = db.Column(db.String(20), nullable=True)
    note = db.Column(db.String(200), nullable=True)
    create_at = db.Column(db.DateTime, default=datetime.now)
    
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(20), nullable=False)
    # payer = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    # 讓花費綁定當下群組
    group_id = create_group_id_column()
    # 使群組能訪問花費資料庫, 才能讓頁面列出花費列表(backref:建立雙向關聯, lazy:關聯參數控制)
    group = db.relationship('Group', backref=db.backref('expense', lazy=True))
    create_at = db.Column(db.DateTime, default=datetime.now)
    
    # 付款人
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # backref創建了一個反向關係，允許後續從 Users 表訪問該用戶支付的所有花費
    payer = db.relationship('User', backref=db.backref('payer_expenses', lazy=True))

    # 分款人
    # secondary指定一個多對多關係資料庫
    # backref 添加反向關係, 會添加一個splitter_expenses在User裡
    # ex. 某用戶A參與了多個Expense, 可通過A.splitter_expenses獲取A參與的所有Expense
    splitters = db.relationship('User', secondary=expense_in_user, backref=db.backref('splitter_expenses', lazy=True))
    
class SettleTheBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=True)
    accounts_receivable = db.Column(db.Integer, nullable=False)
    group_id = create_group_id_column()
    create_at = db.Column(db.DateTime, default=datetime.now)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    group_id = create_group_id_column()
    create_at = db.Column(db.DateTime, default=datetime.now)
    
    