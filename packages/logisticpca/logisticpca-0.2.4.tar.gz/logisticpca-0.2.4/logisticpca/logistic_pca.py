import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class LogisticPCA(nn.Module):
    """
    Standard Logistic PCA for binary data.
    
    Attributes:
        n_features (int): Number of input features (d).
        n_components (int): Number of principal components (k).
    """
    def __init__(self, n_features, n_components, m=5):
        super(LogisticPCA, self).__init__()
        self.n_components = n_components
        self.m = m  

        # Parameters
        self.mu = nn.Parameter(torch.zeros(n_features))  
        self.U = nn.Parameter(torch.randn(n_features, n_components) * 0.01)  

    def forward(self, X):
        theta_tilde = self.m * (2 * X - 1)
        Z = torch.matmul(theta_tilde - self.mu, self.U)
        theta_hat = self.mu + torch.matmul(Z, self.U.T)  

        P_hat = torch.sigmoid(theta_hat)
        return P_hat, theta_hat

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.BCELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            P_hat, _ = self.forward(X)
            loss = criterion(P_hat, X)
            loss.backward()
            optimizer.step()

            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.4f}")

    def transform(self, X):
        with torch.no_grad():
            theta_tilde = self.m * (2 * X - 1)
            Z = torch.matmul(theta_tilde - self.mu, self.U)
            return Z.numpy()

    def inverse_transform(self, X_low_dim):
        with torch.no_grad():
            theta_hat_reconstructed = self.mu + torch.matmul(X_low_dim, self.U.T)
            P_hat_reconstructed = torch.sigmoid(theta_hat_reconstructed)
            return P_hat_reconstructed.numpy()


class SparseLogisticPCA(nn.Module):
    """
    Sparse Logistic PCA with L1 regularization for binary data.
    
    Attributes:
        n_features (int): Number of input features (d).
        n_components (int): Number of principal components (k).
        lambda_L1 (float): Regularization strength for sparsity.
    """
    def __init__(self, n_features, n_components, m=5, lambda_L1=0.01):
        super(SparseLogisticPCA, self).__init__()
        self.n_components = n_components
        self.m = m  
        self.lambda_L1 = lambda_L1  

        # Parameters
        self.mu = nn.Parameter(torch.zeros(n_features))  
        self.U = nn.Parameter(torch.randn(n_features, n_components) * 0.01)  

    def forward(self, X):
        theta_tilde = self.m * (2 * X - 1)  
        Z = torch.matmul(theta_tilde - self.mu, self.U)  
        theta_hat = self.mu + torch.matmul(Z, self.U.T)  

        P_hat = torch.sigmoid(theta_hat)
        return P_hat, theta_hat

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.BCELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            P_hat, _ = self.forward(X)
            loss = criterion(P_hat, X)

            # Add L1 sparsity penalty
            l1_penalty = self.lambda_L1 * torch.norm(self.U, p=1)  
            loss += l1_penalty
            
            loss.backward()
            optimizer.step()

            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.4f}, L1 Penalty: {l1_penalty.item():.4f}")

    def transform(self, X):
        with torch.no_grad():
            theta_tilde = self.m * (2 * X - 1)
            Z = torch.matmul(theta_tilde - self.mu, self.U)
            return Z.numpy()

    def inverse_transform(self, X_low_dim):
        with torch.no_grad():
            theta_hat_reconstructed = self.mu + torch.matmul(X_low_dim, self.U.T)
            P_hat_reconstructed = torch.sigmoid(theta_hat_reconstructed)
            return P_hat_reconstructed.numpy()
            
            
            
class LatentSparseLogisticPCA(nn.Module):
    """
    Logistic PCA with L1 regularization on latent factors (Z) for binary data.

    Attributes:
        n_features (int): Number of input features (d).
        n_components (int): Number of principal components (k).
        lambda_L1 (float): Regularization strength on Z.
    """
    def __init__(self, n_features, n_components, m=5, lambda_L1=0.01):
        super(LatentSparseLogisticPCA, self).__init__()
        self.n_components = n_components
        self.m = m
        self.lambda_L1 = lambda_L1

        # Parameters
        self.mu = nn.Parameter(torch.zeros(n_features))
        self.U = nn.Parameter(torch.randn(n_features, n_components) * 0.01)

    def forward(self, X):
        theta_tilde = self.m * (2 * X - 1)
        Z = torch.matmul(theta_tilde - self.mu, self.U)
        theta_hat = self.mu + torch.matmul(Z, self.U.T)
        P_hat = torch.sigmoid(theta_hat)
        return P_hat, Z

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.BCELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            P_hat, Z = self.forward(X)
            loss = criterion(P_hat, X)

            # L1 regularization on Z (latent scores)
            l1_penalty = self.lambda_L1 * torch.norm(Z, p=1)
            loss += l1_penalty

            loss.backward()
            optimizer.step()

            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.4f}, L1(Z) Penalty: {l1_penalty.item():.4f}")

    def transform(self, X):
        with torch.no_grad():
            theta_tilde = self.m * (2 * X - 1)
            Z = torch.matmul(theta_tilde - self.mu, self.U)
            return Z.numpy()

    def inverse_transform(self, X_low_dim):
        with torch.no_grad():
            theta_hat = self.mu + torch.matmul(X_low_dim, self.U.T)
            return torch.sigmoid(theta_hat).numpy()

import torch
import torch.nn as nn
import torch.optim as optim

class LogisticPCA_SVT(nn.Module):
    """
    Logistic PCA with GDP-penalized low-rank logit structure.
    Based on: Song et al., Chemometrics and Intelligent Laboratory Systems, 2020.

    Θ = 1μᵀ + ABᵀ is the natural parameter matrix (logits), 
    P = sigmoid(Θ) is the probability matrix for Bernoulli likelihood.

    GDP penalty is applied to the singular values of Z = ABᵀ to reduce overfitting.
    """
    def __init__(self, n_samples, n_features, n_components, gamma=1.0, lambda_reg=0.1):
        super().__init__()
        self.n_samples = n_samples
        self.n_features = n_features
        self.n_components = n_components
        self.gamma = gamma
        self.lambda_reg = lambda_reg

        self.A = nn.Parameter(torch.randn(n_samples, n_components) * 0.01)  # Scores (latent rows)
        self.B = nn.Parameter(torch.randn(n_features, n_components) * 0.01)  # Loadings (latent cols)
        self.mu = nn.Parameter(torch.zeros(n_features))  # Intercept (logit of marginals)

    def forward(self):
        Z = torch.matmul(self.A, self.B.T)  # Low-rank matrix Z
        Theta = Z + self.mu  # Broadcasting mu as 1μᵀ
        P = torch.sigmoid(Theta)
        return P, Z

    def compute_loss(self, X):
        P, Z = self.forward()
        bce = nn.BCELoss()(P, X)

        # GDP penalty on singular values of Z
        _, S, _ = torch.linalg.svd(Z, full_matrices=False)
        gdp_penalty = torch.sum(torch.log1p(S / self.gamma))

        return bce + self.lambda_reg * gdp_penalty

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        for epoch in range(epochs):
            optimizer.zero_grad()
            loss = self.compute_loss(X)
            loss.backward()
            optimizer.step()
            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs} | Loss: {loss.item():.4f}")

    def transform(self, A_tensor=None):
        with torch.no_grad():
            A_out = self.A if A_tensor is None else A_tensor
            return A_out.detach().cpu().numpy()

    def inverse_transform(self, A_tensor=None):
        with torch.no_grad():
            A_in = self.A if A_tensor is None else A_tensor
            Theta = torch.matmul(A_in, self.B.T) + self.mu
            return torch.sigmoid(Theta).detach().cpu().numpy()


