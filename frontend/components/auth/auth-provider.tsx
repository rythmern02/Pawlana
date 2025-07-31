import { createContext, type PropsWithChildren, use, useMemo } from 'react'
import { useMobileWallet } from '@/components/solana/use-mobile-wallet'
import { AppConfig } from '@/constants/app-config'
import { Account, useAuthorization } from '@/components/solana/use-authorization'
import { useMutation } from '@tanstack/react-query'

export interface AuthState {
  isAuthenticated: boolean
  isLoading: boolean
  signIn: (username: string, email: string) => Promise<Account>
  signOut: () => Promise<void>
}

const Context = createContext<AuthState>({} as AuthState)

export function useAuth() {
  const value = use(Context)
  if (!value) {
    throw new Error('useAuth must be wrapped in a <AuthProvider />')
  }
  return value
}

function useSignInMutation() {
  const { signIn } = useMobileWallet()

  return useMutation({
    mutationFn: async ({
      username,
      email,
    }: {
      username: string
      email: string
    }) => {
      const account = await signIn({
        uri: AppConfig.uri,
      })

      await fetch(`${AppConfig.apiBaseUrl}/wallet-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          wallet_address: account.publicKey.toString(),
          username,
          email_address: email,
        }),
      })

      return account
    },
  })
}

export function AuthProvider({ children }: PropsWithChildren) {
  const { disconnect } = useMobileWallet()
  const { accounts, isLoading } = useAuthorization()
  const signInMutation = useSignInMutation()

  const value: AuthState = useMemo(
    () => ({
      signIn: async (username: string, email: string) =>
        await signInMutation.mutateAsync({ username, email }),
      signOut: async () => await disconnect(),
      isAuthenticated: (accounts?.length ?? 0) > 0,
      isLoading: signInMutation.isPending || isLoading,
    }),
    [accounts, disconnect, signInMutation, isLoading]
  )

  return <Context value={value}>{children}</Context>
}
