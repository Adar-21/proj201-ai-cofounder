import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '../contexts/AuthContext';
import api from '../utils/api';
import { Ionicons } from '@expo/vector-icons';
import { format } from 'date-fns';

export default function RequestsScreen() {
  const { user } = useAuth();
  const router = useRouter();
  const [requests, setRequests] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      if (user?.role === 'user') {
        const [requestsRes, bookingsRes] = await Promise.all([
          api.get('/service-requests'),
          api.get('/bookings'),
        ]);
        setRequests(requestsRes.data);
        setBookings(bookingsRes.data);
      } else {
        const bookingsRes = await api.get('/bookings');
        setBookings(bookingsRes.data);
      }
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'created':
        return '#FFA500';
      case 'booked':
        return '#007AFF';
      case 'in_progress':
        return '#FF6B6B';
      case 'completed':
        return '#4CAF50';
      default:
        return '#999';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'created':
        return 'time-outline';
      case 'booked':
        return 'calendar-outline';
      case 'in_progress':
        return 'hammer-outline';
      case 'completed':
        return 'checkmark-circle-outline';
      default:
        return 'help-circle-outline';
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  const allItems = user?.role === 'user' 
    ? [...requests, ...bookings].sort((a, b) => 
        new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      )
    : bookings.sort((a, b) => 
        new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>My {user?.role === 'user' ? 'Requests' : 'Jobs'}</Text>
      </View>

      {allItems.length === 0 ? (
        <View style={styles.emptyState}>
          <Ionicons name="document-outline" size={64} color="#ccc" />
          <Text style={styles.emptyText}>
            {user?.role === 'user' ? 'No requests yet' : 'No jobs yet'}
          </Text>
          <Text style={styles.emptySubtext}>
            {user?.role === 'user' 
              ? 'Create your first repair request'
              : 'Wait for job assignments'}
          </Text>
        </View>
      ) : (
        <FlatList
          data={allItems}
          keyExtractor={(item) => item.id}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
          renderItem={({ item }) => (
            <TouchableOpacity
              style={styles.card}
              onPress={() => {
                if (item.serviceRequestId) {
                  router.push(`/booking/${item.id}`);
                } else {
                  router.push(`/service-request/${item.id}`);
                }
              }}
            >
              <View style={styles.cardHeader}>
                <View
                  style={[
                    styles.statusBadge,
                    { backgroundColor: getStatusColor(item.status) },
                  ]}
                >
                  <Ionicons
                    name={getStatusIcon(item.status)}
                    size={16}
                    color="#fff"
                  />
                  <Text style={styles.statusText}>{item.status}</Text>
                </View>
                <Text style={styles.dateText}>
                  {format(new Date(item.createdAt), 'MMM dd, yyyy')}
                </Text>
              </View>

              {item.descriptionText ? (
                <>
                  <Text style={styles.cardTitle}>{item.category || 'Uncategorized'}</Text>
                  <Text style={styles.cardDescription} numberOfLines={2}>
                    {item.descriptionText}
                  </Text>
                </>
              ) : (
                <>
                  <Text style={styles.cardTitle}>Booking</Text>
                  <Text style={styles.cardDescription}>
                    {item.technicianName || 'Technician assigned'}
                  </Text>
                  <Text style={styles.cardPrice}>{item.estimatedPrice}</Text>
                </>
              )}

              <View style={styles.cardFooter}>
                <Ionicons name="chevron-forward" size={20} color="#007AFF" />
              </View>
            </TouchableOpacity>
          )}
          contentContainerStyle={styles.listContent}
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    padding: 20,
    paddingTop: 60,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
  },
  listContent: {
    padding: 16,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  statusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
    marginLeft: 4,
    textTransform: 'capitalize',
  },
  dateText: {
    fontSize: 12,
    color: '#999',
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
    textTransform: 'capitalize',
  },
  cardDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  cardPrice: {
    fontSize: 16,
    fontWeight: '600',
    color: '#4CAF50',
    marginTop: 8,
  },
  cardFooter: {
    marginTop: 12,
    alignItems: 'flex-end',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  emptyText: {
    fontSize: 20,
    fontWeight: '600',
    color: '#666',
    marginTop: 16,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    marginTop: 8,
    textAlign: 'center',
  },
});
