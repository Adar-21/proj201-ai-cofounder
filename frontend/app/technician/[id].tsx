import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import api from '../utils/api';
import { format } from 'date-fns';

export default function TechnicianDetailScreen() {
  const { id, requestId } = useLocalSearchParams();
  const router = useRouter();
  const [technician, setTechnician] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedSlot, setSelectedSlot] = useState('');
  const [booking, setBooking] = useState(false);

  useEffect(() => {
    loadTechnician();
  }, []);

  const loadTechnician = async () => {
    try {
      const response = await api.get(`/technicians/${id}`);
      setTechnician(response.data);
      if (response.data.availabilitySlots?.[0]) {
        setSelectedSlot(response.data.availabilitySlots[0]);
      }
    } catch (error) {
      console.error('Error loading technician:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBooking = async () => {
    if (!selectedSlot) {
      Alert.alert('Error', 'Please select a time slot');
      return;
    }

    setBooking(true);
    try {
      // Get user address (simplified for MVP)
      const userResponse = await api.get('/auth/me');
      const address = userResponse.data.address || 'Istanbul';

      const response = await api.post('/bookings', {
        serviceRequestId: requestId,
        technicianId: id,
        scheduledTime: selectedSlot,
        address,
        estimatedPrice: technician.basePricingInfo?.split('-')[0] || '$100',
      });

      Alert.alert(
        'Booking Confirmed!',
        'Your technician has been notified and will arrive at the scheduled time.',
        [
          {
            text: 'View Booking',
            onPress: () => router.replace(`/booking/${response.data.id}`),
          },
        ]
      );
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Booking failed');
    } finally {
      setBooking(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  if (!technician) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Technician not found</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color="#333" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Technician Profile</Text>
        <View style={{ width: 24 }} />
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        {/* Profile Section */}
        <View style={styles.profileCard}>
          <View style={styles.avatarLarge}>
            <Ionicons name="person" size={48} color="#007AFF" />
          </View>
          <View style={styles.nameContainer}>
            <Text style={styles.name}>{technician.name}</Text>
            {technician.verifiedStatus && (
              <View style={styles.verifiedRow}>
                <Ionicons name="checkmark-circle" size={20} color="#4CAF50" />
                <Text style={styles.verifiedText}>Verified</Text>
              </View>
            )}
          </View>
          <View style={styles.ratingContainer}>
            <Ionicons name="star" size={24} color="#FFA500" />
            <Text style={styles.ratingLarge}>
              {technician.ratingAverage?.toFixed(1)}
            </Text>
            <Text style={styles.reviewCount}>({technician.reviewsCount} reviews)</Text>
          </View>
        </View>

        {/* Categories */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Specialties</Text>
          <View style={styles.categoriesContainer}>
            {technician.categories?.map((category: string, idx: number) => (
              <View key={idx} style={styles.categoryTag}>
                <Text style={styles.categoryTagText}>{category}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Skills */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Skills & Experience</Text>
          <Text style={styles.skillsText}>{technician.skills}</Text>
        </View>

        {/* Pricing */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Estimated Pricing</Text>
          <View style={styles.priceCard}>
            <Ionicons name="cash-outline" size={24} color="#4CAF50" />
            <Text style={styles.priceText}>{technician.basePricingInfo}</Text>
          </View>
        </View>

        {/* Service Areas */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Service Areas</Text>
          <View style={styles.areasContainer}>
            {technician.serviceAreas?.map((area: string, idx: number) => (
              <View key={idx} style={styles.areaTag}>
                <Ionicons name="location-outline" size={14} color="#007AFF" />
                <Text style={styles.areaText}>{area}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Available Slots */}
        {requestId && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Available Time Slots</Text>
            {technician.availabilitySlots?.map((slot: string, idx: number) => (
              <TouchableOpacity
                key={idx}
                style={[
                  styles.slotButton,
                  selectedSlot === slot && styles.slotButtonActive,
                ]}
                onPress={() => setSelectedSlot(slot)}
              >
                <Ionicons
                  name="calendar-outline"
                  size={20}
                  color={selectedSlot === slot ? '#007AFF' : '#666'}
                />
                <Text
                  style={[
                    styles.slotText,
                    selectedSlot === slot && styles.slotTextActive,
                  ]}
                >
                  {format(new Date(slot), 'EEE, MMM dd, yyyy - hh:mm a')}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        )}

        {/* Reviews */}
        {technician.reviews && technician.reviews.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Recent Reviews</Text>
            {technician.reviews.slice(0, 3).map((review: any, idx: number) => (
              <View key={idx} style={styles.reviewCard}>
                <View style={styles.reviewHeader}>
                  <Text style={styles.reviewerName}>{review.userName || 'Customer'}</Text>
                  <View style={styles.reviewRating}>
                    <Ionicons name="star" size={14} color="#FFA500" />
                    <Text style={styles.reviewRatingText}>{review.rating}</Text>
                  </View>
                </View>
                <Text style={styles.reviewText}>{review.comment}</Text>
              </View>
            ))}
          </View>
        )}
      </ScrollView>

      {/* Book Button */}
      {requestId && (
        <View style={styles.footer}>
          <TouchableOpacity
            style={[styles.bookButton, booking && styles.bookButtonDisabled]}
            onPress={handleBooking}
            disabled={booking}
          >
            {booking ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <>
                <Ionicons name="calendar" size={24} color="#fff" />
                <Text style={styles.bookButtonText}>Book Appointment</Text>
              </>
            )}
          </TouchableOpacity>
        </View>
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
  profileCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    marginBottom: 16,
  },
  avatarLarge: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#E3F2FD',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  nameContainer: {
    alignItems: 'center',
    marginBottom: 12,
  },
  name: {
    fontSize: 24,
    fontWeight: '700',
    color: '#333',
    marginBottom: 8,
  },
  verifiedRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  verifiedText: {
    fontSize: 14,
    color: '#4CAF50',
    fontWeight: '600',
    marginLeft: 4,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  ratingLarge: {
    fontSize: 28,
    fontWeight: '700',
    color: '#333',
    marginLeft: 8,
  },
  reviewCount: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
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
  categoriesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  categoryTag: {
    backgroundColor: '#E3F2FD',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 8,
    marginBottom: 8,
  },
  categoryTagText: {
    fontSize: 14,
    color: '#007AFF',
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  skillsText: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
  priceCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0FDF4',
    padding: 16,
    borderRadius: 12,
  },
  priceText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#4CAF50',
    marginLeft: 12,
  },
  areasContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  areaTag: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f9f9f9',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginRight: 8,
    marginBottom: 8,
  },
  areaText: {
    fontSize: 14,
    color: '#007AFF',
    marginLeft: 4,
  },
  slotButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderWidth: 2,
    borderColor: '#ddd',
    borderRadius: 12,
    marginBottom: 12,
    backgroundColor: '#f9f9f9',
  },
  slotButtonActive: {
    borderColor: '#007AFF',
    backgroundColor: '#E3F2FD',
  },
  slotText: {
    fontSize: 16,
    color: '#666',
    marginLeft: 12,
  },
  slotTextActive: {
    color: '#007AFF',
    fontWeight: '600',
  },
  reviewCard: {
    padding: 16,
    backgroundColor: '#f9f9f9',
    borderRadius: 12,
    marginBottom: 12,
  },
  reviewHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  reviewerName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  reviewRating: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  reviewRatingText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
  },
  reviewText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  footer: {
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: '#eee',
    backgroundColor: '#fff',
  },
  bookButton: {
    flexDirection: 'row',
    backgroundColor: '#007AFF',
    padding: 18,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  bookButtonDisabled: {
    opacity: 0.6,
  },
  bookButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 8,
  },
});
