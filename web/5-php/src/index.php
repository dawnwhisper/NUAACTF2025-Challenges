<?php
highlight_file(__FILE__);
class Gateway {
    public $router;
    public function execute() {
        $this->router->redirect();
    }
}

class Dispatcher {
    public $target;
    public function redirect() {
        file_put_contents('temp.log', $this->target);
    }
}

class FileLoader {
    public $path;
    public function __toString() {
        system('whoami');
        include($this->path);
        return '';
    }
}

class Trigger {
    public $handler;
    public function __destruct() {
        $this->handler->execute();
    }
}

$data = $_GET['data'];
unserialize(base64_decode($data));
