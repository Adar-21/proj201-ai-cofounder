import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  ActivityIndicator,
  Image,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import api from '../utils/api';

export default function ServiceRequestDetailScreen() {
  const { id } = useLocalSearchParams();
  const router = useRouter();
  const [request, setRequest] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRequest();
  }, []);

  const loadRequest = async () => {
    try {
      const response = await api.get(`/service-requests/${id}`);
      setRequest(response.data);
    } catch (error) {
      console.error('Error loading request:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  if (!request) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Request not found</Text>
      </View>
    );
  }

  const getConfidenceColor = (confidence: string) => {
    switch (confidence) {
      case 'high':
        return '#4CAF50';
      case 'medium':
        return '#FFA500';
      case 'low':
        return '#FF6B6B';
      default:
        return '#999';
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color="#333" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Request Details</Text>
        <View style={{ width: 24 }} />
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        {/* AI Analysis Result */}
        <View style={styles.aiCard}>
          <View style={styles.aiHeader}>
            <Ionicons name="sparkles" size={24} color="#007AFF" />
            <Text style={styles.aiTitle}>AI Analysis</Text>
          </View>
          
          <View style={styles.aiContent}>
            <View style={styles.categoryBadge}>
              <Text style={styles.categoryText}>
                {request.aiSuggestedCategory?.toUpperCase() || 'OTHER'}
              </Text>
            </View>
            
            <Text style={styles.aiSummary}>{request.aiSummary}</Text>
            
            <View style={styles.confidenceRow}>
              <Text style={styles.confidenceLabel}>Confidence:</Text>
              <View
                style={[
                  styles.confidenceBadge,
                  { backgroundColor: getConfidenceColor(request.aiConfidence) },
                ]}
              >
                <Text style={styles.confidenceText}>
                  {request.aiConfidence?.toUpperCase()}
                </Text>
              </View>
            </View>
          </View>

          <View style={styles.disclaimer}>
            <Ionicons name="information-circle-outline" size={16} color="#666" />
            <Text style={styles.disclaimerText}>
              This is an estimate. Final diagnosis will be done by the professional.
            </Text>
          </View>
        </View>

        {/* Your Description */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Your Description</Text>
          <Text style={styles.descriptionText}>{request.descriptionText}</Text>
        </View>

        {/* Photos */}
        {request.mediaUrls && request.mediaUrls.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Photos</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {request.mediaUrls.map((url: string, index: number) => (
                <Image key={index} source={{ uri: url }} style={styles.photo} />
              ))}
            </ScrollView>
          </View>
        )}

        {/* Urgency */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Urgency</Text>
          <View
            style={[
              styles.urgencyBadge,
              {
                backgroundColor:
                  request.urgency === 'urgent' ? '#FFE5E5' : '#E3F2FD',
              },
            ]}
          >
            <Ionicons
              name={request.urgency === 'urgent' ? 'flash' : 'time'}
              size={20}
              color={request.urgency === 'urgent' ? '#FF3B30' : '#007AFF'}
            />
            <Text
              style={[
                styles.urgencyText,
                {
                  color: request.urgency === 'urgent' ? '#FF3B30' : '#007AFF',
                },
              ]}
            >
              {request.urgency === 'urgent' ? 'Urgent' : 'Normal'}
            </Text>
          </View>
        </View>

        {/* Action Button */}
        {request.status === 'created' && (
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={() => router.push(`/technician-matches/${id}`)}
          >
            <Ionicons name="people" size={24} color="#fff" />
            <Text style={styles.primaryButtonText}>Find Technicians</Text>
          </TouchableOpacity>
        )}

        {request.status === 'booked' && (
          <View style={styles.statusCard}>
            <Ionicons name="checkmark-circle" size={48} color="#4CAF50" />
            <Text style={styles.statusTitle}>Booking Confirmed!</Text>
            <Text style={styles.statusText}>
              Your technician has been notified
            </Text>
          </View>
        )}
      </ScrollView>
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    paddingTop: 60,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#333',
  },
  content: {
    padding: 16,
  },
  aiCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    borderWidth: 2,
    borderColor: '#007AFF',
  },
  aiHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  aiTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#007AFF',
    marginLeft: 8,
  },
  aiContent: {
    marginBottom: 16,
  },
  categoryBadge: {
    alignSelf: 'flex-start',
    backgroundColor: '#007AFF',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    marginBottom: 12,
  },
  categoryText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  aiSummary: {
    fontSize: 16,
    color: '#333',
    lineHeight: 24,
    marginBottom: 12,
  },
  confidenceRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  confidenceLabel: {
    fontSize: 14,
    color: '#666',
    marginRight: 8,
  },
  confidenceBadge: {
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  confidenceText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  disclaimer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    padding: 12,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
  },
  disclaimerText: {
    flex: 1,
    fontSize: 12,
    color: '#666',
    marginLeft: 8,
    lineHeight: 18,
  },
  section: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  descriptionText: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
  photo: {
    width: 150,
    height: 150,
    borderRadius: 12,
    marginRight: 12,
  },
  urgencyBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
  },
  urgencyText: {
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  primaryButton: {
    flexDirection: 'row',
    backgroundColor: '#007AFF',
    padding: 20,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 8,
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 8,
  },
  statusCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 32,
    alignItems: 'center',
  },
  statusTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: '#333',
    marginTop: 16,
  },
  statusText: {
    fontSize: 16,
    color: '#666',
    marginTop: 8,
  },
});
