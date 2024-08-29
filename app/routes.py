from flask import Blueprint, render_template, request, redirect, jsonify
from . import db
from .models import Group, Expense, User, expense_in_user
from sqlalchemy import func
from collections import defaultdict
from sqlalchemy.orm import joinedload


main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return 'Hello Flask!'

@main.route('/group', methods=['POST'])
def create_group():
    data = request.get_json()
    group_name = data.get('groupName')
    
    if not group_name:
        return jsonify({'message': 'The group name is required'}), 400
    
    new_group = Group(name=data['groupName'], note=data['note'])
    
    db.session.add(new_group)
    db.session.commit()
    response = jsonify({'message': 'Group created successfully', 'id': new_group.id})
    
    return response, 201

@main.route('/group/<int:group_id>/add_users', methods=['POST'])
def add_users(group_id):
    data = request.get_json()
    add_user = User(name=data['name'],group_id=group_id)
    db.session.add(add_user)
    db.session.commit()
    response = jsonify({'message': 'User created successfully'})
    return response, 201
    
@main.route('/group/<int:group_id>', methods=['GET'])
# id由<int:id>傳遞
def get_group(group_id):
    # .get位根據主鍵查找資料
    group = Group.query.get(group_id)
    if group:
        response_data = {
            'id': group.id,
            'groupName': group.name,
            'groupNote': group.note
        }
        return jsonify(response_data), 200
    else:
        return jsonify({'message': 'Group not found'}), 404
    
@main.route('/group/<int:group_id>/add_expense', methods=['POST'])
def add_expense(group_id):
    data = request.get_json()

    # 從user資料庫查找前端給的付款人名稱
    payer = User.query.filter_by(name=data['payer']).first()
    
    add_expense = Expense(item=data['item'], amount=data['amount'], group_id=group_id, payer_id=payer.id)
    
    # 從user資料庫查找前端給的分款人名稱
    splitter_names = data.get('splitters', [])
    splitters = User.query.filter(User.name.in_(splitter_names)).all()
    
    # 先新增關聯表資料庫
    add_expense.splitters.extend(splitters)
    db.session.add(add_expense)
    db.session.commit()
    response = jsonify({'message': 'Expense created successfully'})
    return response, 201

@main.route('/group/<int:group_id>/expenses', methods=['GET'])
def get_group_expenses(group_id):
    expenses = Expense.query.filter_by(group_id=group_id).all()
    
    expenses_list = []
    # 找到每筆消費有哪些分帳人
    for expense in expenses:
        splitters = expense.splitters
        splitter_info = [
            {
                'id': splitter.id,
                'name': splitter.name
            } for splitter in splitters
        ]
        
        expenses_list.append(
        {
            'id': expense.id,
            'item': expense.item,
            'amount': expense.amount,
            'payer_id': expense.payer_id,
            'payer': expense.payer.name,
            'splitter_count': len(expense.splitters),
            'splitters': splitter_info
        })
    
    # 後端檢查用
    print(f'get_group_expense_list:')
    for expense in expenses_list:
        print(f'{expense} \n')
    print(f'=============================================')
    
    return jsonify(expenses_list), 200

@main.route('/group/<int:group_id>/settle_the_balance', methods=['POST', 'GET'])
def settle_the_balance(group_id):
    # * step.1 查詢每人應收總額 
    user_balance_dict = {}
    
    receivable_per_user = db.session.query(Expense.payer_id, Expense.id.label('expense_id'), Expense.amount).filter_by(group_id=group_id).all()
    
    for payer_id, expense_id, amount in receivable_per_user:
        if payer_id not in user_balance_dict:
            user_balance_dict[payer_id] = { 'receivable': 0, 'owed': 0 }
            
        user_balance_dict[payer_id]['receivable'] += amount
    
    # 獲取所有參與分帳的用戶, distinct去重複
    # 從expense_in_user抓取到user_id
    # expense_id對應到Expense.id 並且expense.group_id = group.id
    all_users = db.session.query(expense_in_user.c.user_id).join(Expense, expense_in_user.c.expense_id == Expense.id).filter(Expense.group_id == group_id).distinct().all()
    
    for user_id, in all_users:
        if user_id not in user_balance_dict:
            user_balance_dict[user_id] = {'receivable': 0, 'owed': 0}
    
    print(f'step.1 user_balance_dict: {user_balance_dict}')
    print(f'=============================================')
    
    
    # * step.2 取得每筆花費的金額
    expenses = Expense.query.filter_by(group_id=group_id).all()
    
    # * step.3 計算每筆花費的分帳金額
    split_amount_dict = {}
    
    for expense in expenses:
        # 計算expense_id出現次數, 去得該筆花費的分帳人數, scalar() 值形成巡並返回技數結果
        splitter_count = db.session.query(func.count(expense_in_user.c.expense_id)).filter_by(expense_id = expense.id).scalar()
        
        # 計算分帳金額 (消費金額 / 分帳人數)
        if splitter_count > 0:
            amount_per_splitter = round(expense.amount / splitter_count, 1)
        else:
            amount_per_splitter = 0
        
        split_amount_dict[expense.id] = amount_per_splitter
        
    print(f'STEP.3 split_amount_dict:{split_amount_dict}')
    print(f'=============================================')
    
    
    # * step.4 統計每人欠款總額
    for expense_id, amount_per_splitter in split_amount_dict.items():
        # 查詢每筆消費有哪些人分帳
        splitters = db.session.query(expense_in_user.c.user_id).filter_by(expense_id=expense_id).all()
        
        print(f'STEP.4 splittersID:{splitters}')

        for splitter in splitters:
            user_id = splitter[0]
            
            # 應收扣除自己的分帳金額
            # 获取当前花费记录
            expense = Expense.query.filter_by(id=expense_id).first()
            
            if user_id == expense.payer_id:
                user_balance_dict[user_id]['receivable'] -= amount_per_splitter
            else:
                user_balance_dict[user_id]['owed'] += amount_per_splitter

    print(f'\n STEP.4 user_balance_dict:{user_balance_dict}')
    print(f'=============================================')
    
    
    # * step.5 結清帳務 (迭代最大欠款人先付給最大應收人)
    # 自我清算
    for user_id, balance in user_balance_dict.items():
        if balance['receivable'] > 0 and balance['owed'] > 0:
            self_settle_amount = min(balance['receivable'], balance['owed'])
            user_balance_dict[user_id]['receivable'] -= self_settle_amount
            user_balance_dict[user_id]['owed'] -= self_settle_amount
            
    # 降序得到最大應收者
    receivers = sorted(user_balance_dict.items(), key=lambda x: x[1]['receivable'], reverse=True)
    # 降序最大欠款者
    debtors = sorted(user_balance_dict.items(), key=lambda x: x[1]['owed'], reverse=True)
    
    print(f'STEP.5 user_balance_dict:{user_balance_dict}\n')
    print(f'STEP.5_before_loop_Receivers: {receivers}\n')
    print(f'STEP.5_before_loop_Debtors: {debtors}')
    print(f'-----------------------------------------')
    
    settlement_steps = []
    
    while_count = 0
    while True:
        num_of_receivers = 0
        for balance in user_balance_dict.values():
            if balance['receivable'] > 0:
                num_of_receivers += 1
                
        if num_of_receivers <= 1:
            break
        
        max_receiver = receivers[0]
        max_debtor = debtors[0]
        
        receiver_id, receiver_balance = max_receiver
        debtor_id, debtor_balance = max_debtor
        
        # 結算金額為雙方債務中絕對值較小者
        amount_to_settle = min(receiver_balance['receivable'], debtor_balance['owed'])
        
        # 儲存兩兩清算的每一步
        settlement_steps.append({
            'receiver_id': receiver_id,
            'debtor_id': debtor_id,
            'amount': amount_to_settle
        })
        
        # 更新欠款與應收額
        user_balance_dict[receiver_id]['receivable'] -= amount_to_settle
        user_balance_dict[debtor_id]['owed'] -= amount_to_settle
        
        # 移除已結清用戶
        if (user_balance_dict[receiver_id]['receivable'] == 0 and user_balance_dict[receiver_id]['owed'] == 0):
            del user_balance_dict[receiver_id]
                        
        if (user_balance_dict[debtor_id]['receivable'] == 0 and user_balance_dict[debtor_id]['owed'] == 0):
            del user_balance_dict[debtor_id]
        
        # 重新排序
        receivers = sorted(user_balance_dict.items(), key=lambda x: x[1]['receivable'], reverse=True)
        
        debtors = sorted(user_balance_dict.items(), key=lambda x: x[1]['owed'], reverse=True)   
        
        while_count += 1
        
        print(f'STEP.5 counting_cycle: {while_count}')
        print(f'STEP.5 Receivers: {receivers}')
        print(f'STEP.5 Debtors: {debtors}') 
        print(f'-----------------------------------------')
    
    while_count += 1
        
    # 儲存最後一筆兩兩清算到清算步驟裡 (因循環結束後最後一筆會存不到)
    settlement_steps.append({
            'receiver_id': receivers[0][0],
            'debtor_id': debtors[0][0],
            'amount': receivers[0][1]['receivable']
        })
    
    print(f'STEP.5 counting_cycle: {while_count}')
    print(f'STEP.5 settle_result:{user_balance_dict}\n')
    print(f'STEP.5 settlement_steps:{settlement_steps}')
    print(f'=============================================')
    
    # * STEP.6 前端處理
    # 從id抓取用戶名, 用set避免重複id
    user_ids = set()
    for step in settlement_steps:
        user_ids.add(step['receiver_id'])
        user_ids.add(step['debtor_id'])
    
    users = db.session.query(User.id, User.name).filter(User.id.in_(user_ids)).all()
    user_name_dict = {user.id: user.name for user in users}    
    
    # 將用戶名插入settlement_steps
    for step in settlement_steps:
        step['receiver_name'] = user_name_dict[step['receiver_id']]
        step['debtor_name'] = user_name_dict[step['debtor_id']]
        
    print(f'STEP 6 settlement_steps: {settlement_steps}\n')
    # print(f'STEP 6 user_balance_dict: {user_balance_dict}')
    # print(f'STEP 6 user_name_dict: {user_name_dict}')
    
    # 按應收人分組
    receivable_summary = {}
    for step in settlement_steps:
        receiver_id = step['receiver_id']
        
        if receiver_id not in receivable_summary:
            receivable_summary[receiver_id] = {
                'receiver_name': step['receiver_name'],
                'total_receivable': 0,
                'debtors': []
            }

        receivable_summary[receiver_id]['total_receivable'] += step['amount']
        receivable_summary[receiver_id]['debtors'].append({
            'debtor_id': step['debtor_id'],
            'debtor_name': step['debtor_name'],
            'amount': step['amount']
        })
    
    summary = list(receivable_summary.values())
    
    # 後端檢查用
    print(f'STEP.6 receivable_summery:')
    for user_id, balance in receivable_summary.items():
        print(f'{user_id}: {balance} \n')
    print(f'STEP.6 summery:')
    for object in summary:
        print(f'{object} \n')
        
    print(f'=============================================')
    
    # summary for SettleTheBalance
    # settlement_steps for Reconciliation
    return jsonify({'summary': summary,
                    'settlement_steps': settlement_steps
                    })
    
@main.route('/group/<int:group_id>/users', methods=['GET'])
def get_group_users(group_id):
    users = User.query.filter_by(group_id=group_id).all()
    users_list = [{'id': user.id, 'name': user.name} for user in users]
    return jsonify(users_list)

@main.route('/group/<int:group_id>/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(group_id, expense_id):
    expense = Expense.query.filter_by(id=expense_id, group_id=group_id).first()
    
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted successfully'}), 200
    else:
        return jsonify({'error': 'Expense not found'}), 404

@main.route('/group/<int:group_id>/expenses/settle_the_balance/reconciliation', methods=['GET'])
def reconciliation(group_id):
    response, status_code= get_group_expenses(group_id)
    group_expenses = response.get_json()
    
    # 先將每筆分帳整理出來
    expenses_per_user = []
    items = []
    items_set = set()
    
    for expense in group_expenses:
        payer_amount = expense['amount']
        split_amount = round(expense['amount'] / expense['splitter_count'], 1)
        payer_included = False # 檢查付款人有無在分帳人名單
        
        
        for splitter in expense['splitters']:
            if expense['payer'] == splitter['name']:
                # 檢查是若為付款人, 要算成(付款金額 - 分攤金額)
                user_expense = (payer_amount - split_amount)
                payer_included = True
            else:
                user_expense = - (split_amount)
                
            expenses_per_user.append({
                'expense_id': expense['id'],
                'user_id': splitter['id'],
                'user_name': splitter['name'],
                'item': expense['item'],
                'expense': user_expense
            })
            items_set.add((expense['id'], expense['item']))
        
        # 付款人不在分帳名單中, 另外單獨記一筆應收款
        if not payer_included:
            expenses_per_user.append({
                    'expense_id': expense['id'],
                    'user_id': expense['payer_id'],
                    'user_name': expense['payer'],
                    'item': expense['item'],
                    'expense': expense['amount']
            })
            items_set.add((expense['id'], expense['item']))
    
    # 前端需要的花費項目列表        
    items = [{'expense_id': item[0], 'expense_item': item[1]} for item in items_set]
    
    # 依使用者分組, 整理每個人的應收與欠款
    # defaultdict自動將不存在的key創建一個空列表
    expenses_by_user = defaultdict(list)
    
    for expenses in expenses_per_user:
        user_name = expenses['user_name']
        expenses_by_user[user_name].append(expenses)
    
    # 轉成普通的dict 
    expenses_by_user = dict(expenses_by_user)
    
    # 計算每人的債務總合
    total_expenses_by_user = {}
    for user_name, expenses in expenses_by_user.items():
        total_expenses = sum(expense['expense'] for expense in expenses)
        total_expenses_by_user[user_name] = total_expenses
     
    # 後端檢查用     
    print(f'expenses_by_user:')
    for user_name, expenses in expenses_by_user.items():
        print(f'\n {user_name}:')
        for expense in expenses:
            print(f'{expense}')
    print(f'\n total_expenses_by_user: {total_expenses_by_user}')
    print(f'\n items:')
    for item in items:
        print(f'{item}')
    print(f'=============================================')
    
    return jsonify({
        'expenses_by_user': expenses_by_user,
        'total_expenses_by_user': total_expenses_by_user,
        'items': items                    
        })
    
@main.route('/expenses/<int:expense_id>/splitters', methods=['GET'])
def get_local_splitters(expense_id):
    '''讓編輯花費時預設選取先前分配好的分帳人'''
    # joinedload會在查詢主物件時，同時加載其關聯物件，減少資料庫查詢次數
    expense = db.session.query(Expense).options(joinedload(Expense.splitters)).filter_by(id=expense_id).first()

    splitter_names = [splitter.name for splitter in expense.splitters]
    
    print(f'get_local_splitters: {splitter_names}')
    print(f'=============================================')
    
    return jsonify(splitter_names)

@main.route('/expenses/<int:expense_id>/update_expense' ,methods=['PUT'])
def update_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'update_expense Error': 'localExpense not found'}), 404
    
    #接收單個數據處理
    data = request.json
    
    # data.get(目標, 否則為)
    expense.item = data.get('item', expense.item)
    expense.amount = data.get('amount', expense.amount)
    
    # Expense中的payer是db.relationship屬性, 不直接儲存數值
    # 故要由前端提供payer --> 查詢User實體 --> 賦值給new_payer
    payer = data.get('payer')
    # .first()返回匹配的第一筆資料, 否則為None
    # 若查詢對象為主鍵(id), 可直接用查詢User.query.get(id)查詢
    new_payer = User.query.filter_by(name=payer).first()
    
    # SQL會自己從查詢到的多個屬性對應
    expense.payer = new_payer
    
    # 更新splitters
    # splitter_names from get_local_splitters()
    # new_splitters的查詢是返回了User的所有屬性(包含id, name等等)
    splitter_names = data.get('splitters', [])
    
    new_splitters = User.query.filter(User.name.in_(splitter_names)).all()

    # 更新多對多資料庫
    # SQLAlchemy 會自動判讀 expense_in_user 裡有哪些屬性要更新
    # 在這裡只有 User 中的 user_id 會更新
    expense.splitters = new_splitters
        
    db.session.commit()
    
    return jsonify({"message": "Expense updated successfully"}), 200

@main.route('/group/<int:group_id>/update_users', methods=['PUT'])
def update_users(group_id):
    
    # 接收列表數據處理
    data = request.json.get('users', [])
    local_users = User.query.filter_by(group_id=group_id).all()
    local_users_dict = {user.id: user for user in local_users}
    
    for user_data in data:
        user_id = user_data.get('id')
        user_name = user_data.get('name')
        
        # 更新現有用戶
        if user_id and user_id in local_users_dict:
            user = local_users_dict[user_id]
            user.name = user_name #SQLAlchemy 會自動出更新回User資料庫
        else:
            # 新增用戶
            new_user = User(name=user_name, group_id=group_id)
            db.session.add(new_user)
    
    db.session.commit()
    
    return jsonify({'message': 'update_users successfully!'}), 200
    
@main.route('/group/<int:group_id>/<int:user_id>', methods=['DELETE'])
def delete_user(group_id, user_id):
    
    local_user = User.query.filter_by(id=user_id).first()
    
    if not local_user:
        return jsonify({'error': 'User not found'}), 404
    
    if local_user.splitter_expenses:
        return jsonify({'error': 'The user has expense and cannot be deleted'}) , 400
    else:
        db.session.delete(local_user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    
@main.route('/my_groups', methods=['GET'])
def get_all_groups():
    groups = Group.query.all()
    groups_list = [{'id': group.id, 'name': group.name} for group in groups]
    return jsonify(groups_list), 200
    
@main.route('/my_groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    group = Group.query.filter_by(id = group_id).first()
    
    expenses_in_group = Expense.query.filter_by(group_id=group.id).all()
    for expense in expenses_in_group:
        expense.splitters.clear() # 先清除多對多關聯
        
    db.session.commit()
    
    for expense in expenses_in_group:
        db.session.delete(expense)
    
    users_in_group = User.query.filter_by(group_id=group_id).all()
    for user in users_in_group:
        db.session.delete(user)
    
    db.session.commit()
        
    db.session.delete(group)
    db.session.commit()
    return jsonify({'message': 'Group deleted successfully'}), 200
    
@main.route('/group/<int:group_id>/update_group', methods=['put'])
def update_group(group_id):
    group = Group.query.filter_by(id=group_id).first()
    
    data = request.json
    group.name = data.get('name', group.name)
    group.note = data.get('note', group.name)
    
    db.session.commit()
    
    return jsonify({'message': 'Group updated successfully'}), 200
        
    
    
    