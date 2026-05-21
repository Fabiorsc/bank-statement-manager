from database.repositories.account_repository import AccountRepository
from database.repositories.account_layout_repository import AccountLayoutRepository
from database.repositories.transaction_repository import TransactionRepository
from database.repositories.import_repository import ImportRepository


RepositoryAccount = AccountRepository()
RepositoryAccountLayout = AccountLayoutRepository()
RepositoryTransaction = TransactionRepository()
RepositoryImport = ImportRepository()

