import { Account, useAuthorization } from '@/components/solana/use-authorization'
import { useMobileWallet } from '@/components/solana/use-mobile-wallet'
import { useMutation } from '@tanstack/react-query'
import { createContext, type PropsWithChildren, use, useMemo } from 'react'

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
      console.log("GMG GM ")
      const account = await signIn({ uri: "https://pawlana.vercel.app" })
      console.log("GMG GM 2 3", account)
      
      try {
        const response = await fetch(`https://pawlana.vercel.app/wallet-login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            wallet_address: account.publicKey.toString(),
            username: "rythme",
            email: "rythmenagrani@gmail.com",
          }),
        })
        
        if (!response.ok) {
          const errorText = await response.text()
          throw new Error(`API failed: ${response.status} - ${errorText}`)
        }
        
        const result = await response.json()
        console.log("API success:", result)
      } catch (error) {
        console.log("API error:", error)
        throw error // Re-throw to fail the mutation
      }

      return account
    },
  })
}

export function AuthProvider({ children }: PropsWithChildren) {
  const { disconnect } = useMobileWallet()
  const { accounts, isLoading } = useAuthorization()
  const signInMutation = useSignInMutation()

  const value: any = useMemo(
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
