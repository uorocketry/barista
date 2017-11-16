require 'minitest/autorun'

class RocketTest < MiniTest::Unit::TestCase

  setup do
    @rocket = Rocket.new
  end

  test 'rocket initial state is ground' do
    assert_equal 'ground', rocket.state
  end
end
