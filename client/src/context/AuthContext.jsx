import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const checkAuthStatus = async () => {
        try {
            const response = await api.get('accounts/me/');
            setUser(response.data.data);
        } catch (error) {
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        checkAuthStatus();
    }, []);

    const login = async (email, password) => {
        const response = await api.post('accounts/login/', { email, password });
        await checkAuthStatus();
        return response.data;
    };

    const register = async (email, password, first_name, last_name) => {
        const response = await api.post('accounts/register/', { email, password, first_name, last_name });
        await checkAuthStatus();
        return response.data;
    };

    const logout = async () => {
        try {
            await api.post('accounts/logout/');
        } finally {
            setUser(null);
        }
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, register, logout, checkAuthStatus }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
