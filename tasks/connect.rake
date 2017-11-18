task :connect do
  namespace :usb do
    sh 'ssh -o StrictHostKeyChecking=no root@192.168.7.2'
  end

  namespace :local do
    sh 'ssh -o StrictHostKeyChecking=no root@192.168.2.117'
  end

  namespace :remote do
    sh 'ssh -o StrictHostKeyChecking=no root@'
  end

end
