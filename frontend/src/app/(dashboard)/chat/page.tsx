import ChatInterface from '@/components/Chat/ChatInterface'

export default function ChatPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">AI Task Assistant</h1>
        <p className="text-gray-600">Manage your tasks using natural language.</p>
      </div>
      <ChatInterface />
    </div>
  )
}
