require "test_helper"
require "minitest/mock"

class HomeControllerTest < ActionDispatch::IntegrationTest

  setup do
    mock_chatgpt = Minitest::Mock.new
    mock_chatgpt.expect(:tweets, [{ content: "Tweet 1", username: "@user1" }], [1])
    Chatgpt.stub(:new, mock_chatgpt) do
    end
  end

  test "should get index" do
    get home_index_url
    assert_response :success
  end
end
