from abc import ABC, abstractmethod

class Conta(ABC):
    def __init__(self, agencia, numero_conta, saldo):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self._saldo = saldo
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
        else:
            raise ValueError('Valor depositado deve ser positivo')

    @abstractmethod
    def sacar(self, valor):
        pass

    def get_saldo(self):
        return self._saldo

class ContaCorrente(Conta):
    def __init__(self, agencia, numero_conta, saldo, limite):
        super().__init__(agencia, numero_conta, saldo)
        self.limite = limite

    def sacar(self, valor):
        if valor <= (self._saldo + self.limite):
            self._saldo -= valor
        else:
            raise ValueError('Saldo insuficiente')

class ContaPoupanca(Conta):
    def __init__(self, agencia, numero_conta, saldo):
        super().__init__(agencia, numero_conta, saldo)

    def sacar(self, valor):
        if valor <= self._saldo:
            self._saldo -= valor
        else:
            raise ValueError('Saldo insuficiente')

class Pessoa(ABC):
    def __init__(self, nome, idade):
        self._nome = nome
        self._idade = idade

    @property
    def nome(self):
        return self._nome
    
    @property
    def idade(self):
        return self._idade
    
class Cliente(Pessoa):
    def __init__(self, nome, idade, conta):
        super().__init__(nome, idade)
        self.conta = conta

    def get_conta(self):
        return self.conta

class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []
        
    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
    def autenticar(self, cliente, conta):
        if cliente in self.clientes and conta in self.contas:
            if cliente.get_conta() == conta:
                return True
        return False

    def realizar_saque(self, cliente, valor):
        conta = cliente.get_conta()
        if self.autenticar(cliente, conta):
            conta.sacar(valor)
        else:
            raise ValueError('Falha na autenticação')
    
    def realizar_deposito(self, cliente, valor):
        conta = cliente.get_conta()
        if self.autenticar(cliente, conta):
            conta.depositar(valor)
        else:
            raise ValueError('Falha na autenticação')
        
# Instanciar contas
conta_corrente = ContaCorrente(agencia="001", numero_conta="12345", saldo=10030.0, limite=500.0)
conta_poupanca = ContaPoupanca(agencia="001", numero_conta="67890", saldo=500.0)

# Instanciar clientes
cliente1 = Cliente(nome="Alice", idade=30, conta=conta_corrente)
cliente2 = Cliente(nome="Bob", idade=40, conta=conta_poupanca)

# Instanciar banco
banco = Banco()

# Adicionar clientes e contas ao banco
banco.adicionar_cliente(cliente1)
banco.adicionar_cliente(cliente2)
banco.adicionar_conta(conta_corrente)
banco.adicionar_conta(conta_poupanca)

# Realizar depósitos
try:
    banco.realizar_deposito(cliente1, 200.0)
    print(f"Depósito realizado. Saldo da conta corrente: {conta_corrente.get_saldo()}")
except ValueError as e:
    print(e)

try:
    banco.realizar_deposito(cliente2, 100.0)
    print(f"Depósito realizado. Saldo da conta poupança: {conta_poupanca.get_saldo()}")
except ValueError as e:
    print(e)

# Realizar saques
try:
    banco.realizar_saque(cliente1, 500.0)
    print(f"Saque realizado. Saldo da conta corrente: {conta_corrente.get_saldo()}")
except ValueError as e:
    print(e)

try:
    banco.realizar_saque(cliente2, 200.0)
    print(f"Saque realizado. Saldo da conta poupança: {conta_poupanca.get_saldo()}")
except ValueError as e:
    print(e)

# Tentativa de saque com saldo insuficiente
try:
    banco.realizar_saque(cliente1, 1500.0)
except ValueError as e:
    print(e)  # Esperado: Saldo insuficiente
