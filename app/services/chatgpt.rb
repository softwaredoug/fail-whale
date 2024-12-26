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
      Return the tweets as a JSON array of objects, each with a "content" and "username" field.
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
    # Attempt to get as array of hashes
    puts content
    resp = JSON.parse(content)
    resp_array = []
    if resp.is_a?(Array) && resp.all?
      resp.each do |item|
        if item.is_a?(Hash) && item.key?("content") && item.key?("username")
        resp_array << item.transform_keys(&:to_sym)
        end
      end
    end
    resp_array
  end
end
