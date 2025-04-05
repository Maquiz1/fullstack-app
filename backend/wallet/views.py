from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Wallet, Transaction
from .serializers import UserSerializer, WalletSerializer, TransactionSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created'}, status=201)
        return Response(serializer.errors, status=400)

class WalletView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = float(request.data['amount'])
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += amount
        wallet.save()
        Transaction.objects.create(wallet=wallet, amount=amount, type='deposit')
        return Response({'message': 'Deposited successfully'})

class PaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = float(request.data['amount'])
        wallet = Wallet.objects.get(user=request.user)
        if wallet.balance >= amount:
            wallet.balance -= amount
            wallet.save()
            Transaction.objects.create(wallet=wallet, amount=amount, type='payment')
            return Response({'message': 'Payment successful'})
        return Response({'error': 'Insufficient balance'}, status=400)

class TransactionHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        transactions = Transaction.objects.filter(wallet=wallet).order_by('-timestamp')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
