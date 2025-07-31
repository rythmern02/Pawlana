import { useState } from 'react'
import { router } from 'expo-router'
import {
  SafeAreaView,
  TextInput,
  View,
  ActivityIndicator,
  StyleSheet,
} from 'react-native'
import { Image } from 'expo-image'
import { Button } from '@react-navigation/elements'

import { useAuth } from '@/components/auth/auth-provider'
import { AppText } from '@/components/app-text'
import { AppView } from '@/components/app-view'
import { AppConfig } from '@/constants/app-config'

export default function SignIn() {
  const { signIn, isLoading } = useAuth()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')

  const handleConnect = async () => {
    try {
      await signIn(username.trim(), email.trim())
      router.replace('/')
    } catch (err) {
      console.error('Sign-in failed:', err)
      // Optionally display a toast or error
    }
  }

  return (
    <AppView style={styles.container}>
      {isLoading ? (
        <ActivityIndicator size="large" color="#FFA500" />
      ) : (
        <SafeAreaView style={styles.safeArea}>
          <View />
          <View style={styles.center}>
            <AppText type="title">{AppConfig.name}</AppText>
            <Image
              source={require('../assets/images/icon.png')}
              style={styles.image}
            />

            <TextInput
              placeholder="Username"
              value={username}
              onChangeText={setUsername}
              style={styles.input}
              autoCapitalize="none"
            />

            <TextInput
              placeholder="Email"
              value={email}
              onChangeText={setEmail}
              style={styles.input}
              autoCapitalize="none"
              keyboardType="email-address"
            />
          </View>
          <View style={styles.footer}>
            <Button variant="filled" style={styles.button} onPress={handleConnect}>
              Connect
            </Button>
          </View>
        </SafeAreaView>
      )}
    </AppView>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'stretch',
  },
  safeArea: {
    flex: 1,
    justifyContent: 'space-between',
  },
  center: {
    alignItems: 'center',
    gap: 16,
    paddingHorizontal: 24,
  },
  image: {
    width: 128,
    height: 128,
    marginVertical: 16,
  },
  input: {
    width: '100%',
    padding: 12,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 10,
    fontSize: 16,
    backgroundColor: '#fff',
  },
  footer: {
    marginBottom: 24,
    paddingHorizontal: 16,
  },
  button: {
    paddingVertical: 12,
  },
})
