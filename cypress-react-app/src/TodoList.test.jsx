import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import axios from 'axios'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { TodoList } from './TodoList'

vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

const credentials = { email: 'user@example.com', password: 'secret123' }

describe('TodoList', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('affiche un état de chargement pendant la récupération des tâches', () => {
    axios.get.mockReturnValue(new Promise(() => {}))

    render(<TodoList credentials={credentials} />)

    expect(screen.getByText('Chargement...')).toBeInTheDocument()
  })

  it('affiche les tâches reçues de l’API', async () => {
    axios.get.mockResolvedValue({
      data: [
        { id: 1, title: 'Première tâche' },
        { id: 2, title: 'Deuxième tâche' },
      ],
    })

    render(<TodoList credentials={credentials} />)

    expect(await screen.findByText('Première tâche')).toBeInTheDocument()
    expect(screen.getByText('Deuxième tâche')).toBeInTheDocument()
    expect(axios.get).toHaveBeenCalledWith(
      'http://localhost:8000/api/tasks/',
      { auth: { username: credentials.email, password: credentials.password } },
    )
  })

  it('affiche un message si la récupération des tâches échoue', async () => {
    axios.get.mockRejectedValue(new Error('API indisponible'))

    render(<TodoList credentials={credentials} />)

    expect(
      await screen.findByText('Impossible de charger les tâches.'),
    ).toBeInTheDocument()
  })

  it('ajoute une tâche et l’affiche après la réponse de l’API', async () => {
    const user = userEvent.setup()
    axios.get.mockResolvedValue({ data: [] })
    axios.post.mockResolvedValue({
      data: { id: 1, title: 'Tâche ajoutée' },
    })

    render(<TodoList credentials={credentials} />)

    await user.type(
      await screen.findByRole('textbox', { name: /nouvelle tâche/i }),
      'Tâche ajoutée',
    )
    await user.click(screen.getByRole('button', { name: /ajouter/i }))

    expect(await screen.findByText('Tâche ajoutée')).toBeInTheDocument()
    expect(axios.post).toHaveBeenCalledWith(
      'http://localhost:8000/api/tasks/',
      { title: 'Tâche ajoutée' },
      { auth: { username: credentials.email, password: credentials.password } },
    )
    expect(screen.getByRole('textbox', { name: /nouvelle tâche/i })).toHaveValue('')
  })
})
