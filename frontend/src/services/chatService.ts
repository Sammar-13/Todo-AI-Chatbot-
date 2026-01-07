import apiClient from '@/utils/api'

export interface ChatRequest {
  conversation_id?: string
  message: string
}

export interface ToolCall {
  tool: string
  args: any
  result: string
}

export interface ChatResponse {
  conversation_id: string
  response: string
  tool_calls: ToolCall[]
}

const chatService = {
  async sendMessage(userId: string, data: ChatRequest): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>(`/api/${userId}/chat`, data)
    return response.data
  }
}

export default chatService
