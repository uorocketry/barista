require 'minitest/autorun'
require_relative '../app/rocket'

class RocketTest < MiniTest::Test

  def setup
    @rocket = Rocket.new
  end

  def test_rocket_initial_state_is_ground
    assert @rocket.ground?
  end
end
