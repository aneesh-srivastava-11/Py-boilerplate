import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';

const Dashboard = () => {
    const { user, logout } = useAuth();
    const [secureData, setSecureData] = useState(null);
    const [error, setError] = useState('');

    const fetchSecureData = async () => {
        try {
            const response = await api.get('accounts/me/');
            setSecureData(response.data);
            setError('');
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to fetch secure data');
            setSecureData(null);
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
            <h2>Dashboard</h2>
            <div>
                <h3>Welcome, {user?.first_name} {user?.last_name} ({user?.email})</h3>
                <button onClick={logout} style={{ marginRight: '10px' }}>Logout</button>
                <button onClick={fetchSecureData}>Test Secure Endpoint (/me)</button>
            </div>

            {error && <p style={{ color: 'red', marginTop: '20px' }}>{error}</p>}

            {secureData && (
                <div style={{ marginTop: '20px', padding: '10px', background: '#f5f5f5', borderRadius: '5px' }}>
                    <h4>Secure Data Response:</h4>
                    <pre>{JSON.stringify(secureData, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
