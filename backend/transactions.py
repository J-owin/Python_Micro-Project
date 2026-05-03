class Transaction():
    def __init__(self,amount,category,t_type,date,description,id=None):
        self.id= id
        self.amount = float(amount)
        self.category = category
        self.t_type = t_type
        self.date = date
        self.description = description
    def __repr__(self):
        return f"Transaction(id={self.id}, amount={self.amount}, category='{self.category}', t_type='{self.t_type}')"