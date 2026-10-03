import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { Login } from './Login'

describe('Login', () => {
  it('désactive le bouton tant que le formulaire est invalide', async () => {
    const user = userEvent.setup()
    render(<Login onLoginSuccess={vi.fn()} />)

    const emailInput = screen.getByPlaceholderText(/email/i)
    const passwordInput = screen.getByPlaceholderText(/mot de passe/i)
    const submitButton = screen.getByRole('button', { name: /se connecter/i })

    expect(submitButton).toBeDisabled()

    await user.type(emailInput, 'email-invalide')
    await user.type(passwordInput, '12345')
    expect(submitButton).toBeDisabled()

    await user.clear(emailInput)
    await user.type(emailInput, 'user@example.com')
    expect(submitButton).toBeDisabled()

    await user.type(passwordInput, '6')
    expect(submitButton).toBeEnabled()
  })

  it('transmet les identifiants lorsque le formulaire est soumis', async () => {
    const user = userEvent.setup()
    const onLoginSuccess = vi.fn()
    render(<Login onLoginSuccess={onLoginSuccess} />)

    await user.type(screen.getByPlaceholderText(/email/i), 'user@example.com')
    await user.type(screen.getByPlaceholderText(/mot de passe/i), 'secret123')
    await user.click(screen.getByRole('button', { name: /se connecter/i }))

    expect(onLoginSuccess).toHaveBeenCalledOnce()
    expect(onLoginSuccess).toHaveBeenCalledWith('user@example.com', 'secret123')
  })
})
