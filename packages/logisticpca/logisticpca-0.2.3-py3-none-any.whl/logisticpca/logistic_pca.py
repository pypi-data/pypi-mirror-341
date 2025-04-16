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
    Logistic PCA using low-rank SVD structure and non-convex GDP penalty to mitigate overfitting,
    as described in Song et al. (2020).

    Attributes:
        n_samples (int): Number of observations (rows).
        n_features (int): Number of binary features (columns).
        n_components (int): Number of principal components (latent dimensions).
        gamma (float): GDP penalty shape parameter.
        lambda_reg (float): Penalty strength.
    """
    def __init__(self, n_samples, n_features, n_components, gamma=1.0, lambda_reg=0.1):
        super().__init__()
        self.n_samples = n_samples
        self.n_features = n_features
        self.n_components = n_components
        self.gamma = gamma
        self.lambda_reg = lambda_reg

        # Latent factor matrices and intercept
        self.A = nn.Parameter(torch.randn(n_samples, n_components) * 0.01)  # scores
        self.B = nn.Parameter(torch.randn(n_features, n_components) * 0.01)  # loadings
        self.mu = nn.Parameter(torch.zeros(n_features))  # column intercept

    def forward(self):
        Z = torch.matmul(self.A, self.B.T)  # Low-rank logit structure
        Theta = self.mu + Z  # Add offset
        P = torch.sigmoid(Theta)
        return P, Z

    def compute_loss(self, X, P, Z):
        bce_loss = nn.BCELoss()(P, X)
        _, S, _ = torch.linalg.svd(Z, full_matrices=False)
        gdp_penalty = torch.sum(torch.log1p(S / self.gamma))
        return bce_loss + self.lambda_reg * gdp_penalty

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        for epoch in range(epochs):
            optimizer.zero_grad()
            P, Z = self.forward()
            loss = self.compute_loss(X, P, Z)
            loss.backward()
            optimizer.step()

            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs} | Loss: {loss.item():.4f}")

    def transform(self, X):
        with torch.no_grad():
            Theta = self.mu + torch.matmul(self.A, self.B.T)
            return self.A.detach().cpu().numpy()

    def inverse_transform(self):
        with torch.no_grad():
            Theta = self.mu + torch.matmul(self.A, self.B.T)
            return torch.sigmoid(Theta).detach().cpu().numpy()

