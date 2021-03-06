import time
from bank import Bank
from gcoin_presenter import GcoinPresenter

RESET_BALANCE = 1000  # in satoshi
INITIAL_BALANCE = 1000000.0
CLEAN_COLOR = 2

gcoin = GcoinPresenter()

def reset_bank_balance(bank, central_bank):
    # bank.merge_tx_in(color=2, div=20)

    # print central_bank
    balance = bank.balance
    diff = float(balance.get(2, 0) - RESET_BALANCE)
    # print 'bank:{}, diff:{}'.format(bank.bank_id, diff)
    if diff < 0:
        print 'CASE 1:', central_bank.send_to(bank, -1 * diff, CLEAN_COLOR)
    elif diff > 0:
        print 'CASE 2:', bank.send_to(central_bank, diff, CLEAN_COLOR)
    elif diff == 0:
        print 'CASE 3: diff = 0'

    if balance.get(1, 0) < 1000000:
        central_bank.send_to(bank, INITIAL_BALANCE, 1)

    print diff, bank.bank_id, bank.address, bank.balance

def main():
    central_bank = Bank.manager.get_central_bank()
    fixed_address = gcoin.get_fixed_address()
    gcoin.mint(1, 0)
    gcoin.mint(1, 0)
   
    time.sleep(90)
   
    should_wait_license = False
    if not gcoin.is_license_exist(1):
        gcoin.create_license(fixed_address, 1)
        should_wait_license = True
    if not gcoin.is_license_exist(2):
        gcoin.create_license(fixed_address, 2)
        should_wait_license = True
   
    if should_wait_license:
        time.sleep(90)
    
    gcoin.mint(7000000000, 1)
    gcoin.mint(7000000000, 2)
    
    time.sleep(90)
    gcoin.send_to_address(central_bank.address, 1000000000, 1)
    gcoin.send_to_address(central_bank.address, 1000000000, 2)

    print 'CB:', central_bank.address, central_bank.balance
    # print 'Bank.manager.bank_list:', Bank.manager.bank_list
    central_bank = Bank.manager.get_central_bank()
    for bank_id in Bank.manager.bank_list:
        bank = Bank.manager.get_bank_by_id(bank_id)
        # print bank.bank_id, bank.balance

        reset_bank_balance(bank, central_bank)


if __name__ == '__main__':
    main()
