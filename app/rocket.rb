class Rocket
  include AASM

  aasm do
    state :ground, initial: true
    event :launch do
      transitions from: :ground, to: :flight
    end

    state :descent
    event :appogee do
      transitions from: :flight, to: :decent
    end

    state :descent_drogue
    event :deploy_drogue do
      transitions from: :descent, to: :recovery_one
    end

    state :descent_main
    event :deploy_main do
      transitions from: :recovery_one, to: :recovery_two, before: :eject_parachute
    end

    event :touchdown do
      transitions from: [:descent_drogue, :descent_main], to: :ground,
    end

    state :idle
    event :sleep do
      transitions from: :ground, to: :power_saver,
    end
  end
end
