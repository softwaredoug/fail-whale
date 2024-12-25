require "openai"

class Chatgpt
  def initialize
    @client = OpenAI::Client.new(
      access_token: ENV["OPENAI_API_KEY"],
      log_errors: true
    )
  end

  def tweets(n)
    prompt = <<~PROMPT
      Generate #{n} unique and creative tweets. Each tweet should include:
      - The content of the tweet
      - A fictional username (@username format)
      Return the tweets as a Ruby array of hashes with keys: `:content` and `:username`.
    PROMPT

    response = @client.chat(
      parameters: {
        model: "gpt-4", # Use the desired OpenAI model
        messages: [ { role: "user", content: prompt } ],
        max_tokens: 500,
        temperature: 0.7
      }
    )
    content = response.dig("choices", 0, "message", "content")
    # Attempt to get as array
    eval(content)
  end
end
