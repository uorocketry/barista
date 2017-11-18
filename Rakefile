desc "Connect to Beaglebone"
namespace :connect do
  task :usb do
    sh 'ssh -o StrictHostKeyChecking=no root@192.168.7.2'
  end

  task :local do
    sh 'ssh -o StrictHostKeyChecking=no root@192.168.2.117'
  end

  task :remote do
    puts "Enter curent port"
    port = gets.chomp
    sh "ssh -l root -p #{port} tcp://0.tcp.ngrok.io"
  end
end
