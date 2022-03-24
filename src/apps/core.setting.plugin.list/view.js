const IS_DEV = wiz.data.IS_DEV;
const BRANCH = wiz.data.BRANCH;
const BRANCHES = wiz.data.BRANCHES;
const API_URL = wiz.API.url("");

let setting_builder = function ($scope, $timeout, $sce) {
    $scope.math = Math;
    $scope.trustAsHtml = $sce.trustAsHtml;
    $scope.loaded = true;

    $scope.env = {}
    $scope.env.branches = BRANCHES;
    $scope.env.branch = BRANCH;

    $scope.modal = {};
    $scope.modal.config = {};
    $scope.modal.message = function (data) {
        $scope.modal.config = data;
        $timeout();
        $('#modal-message').modal('show');
    };

    $scope.modal.message.hide = function () {
        $scope.modal.config = {};
        $timeout();
        $('#modal-message').modal('hide');
    }
}

let wiz_controller = async ($sce, $scope, $timeout) => {
    _builder($scope, $timeout);
    setting_builder($scope, $timeout, $sce);

    let API = {
        handler: (resolve, reject) => async (res) => {
            if (res.code == 200) resolve(res.data);
            else reject(res);
        },
        list: () => new Promise((resolve, reject) => {
            let url = wiz.API.url("list");
            $.get(url, API.handler(resolve, reject));
        }),
        install: (data) => new Promise((resolve, reject) => {
            let url = wiz.API.url("install");
            data = angular.copy(data);
            $.post(url, data, resolve);
        }),
        create: (data) => new Promise((resolve, reject) => {
            let url = wiz.API.url("create");
            data = angular.copy(data);
            $.post(url, data, resolve);
        }),
        download: (data) => new Promise((resolve, reject) => {
            let url = wiz.API.url("export");
            data = angular.copy(data);
            $.post(url, data, resolve);
        }),
        timeout: (ts) => new Promise((resolve) => {
            $timeout(resolve, ts);
        })
    };

    $scope.math = Math;

    $scope.list = [];
    $scope.event = {};

    $scope.event.load = async () => {
        let data = await API.list();

        $scope.list = data;
        $scope.list.sort((a, b) => {
            let comp = 0;
            try {
                comp = a.name.localeCompare(b.name);
                if (comp != 0) return comp;
            } catch (e) { }
            comp = a.id.localeCompare(b.id);
            return comp;
        });

        await API.timeout();
    }

    $scope.event.search = async (val) => {
        val = val.toLowerCase();
        for (var i = 0; i < $scope.list.length; i++) {
            if (val.length == 0) {
                $scope.list[i].hide = false;
                continue;
            }

            let searchindex = ['name', 'id', 'author_name'];
            $scope.list[i].hide = true;
            for (let j = 0; j < searchindex.length; j++) {
                try {
                    let key = searchindex[j];
                    let keyv = $scope.list[i][key].toLowerCase();
                    if (keyv.includes(val)) {
                        $scope.list[i].hide = false;
                        break;
                    }
                } catch (e) {
                }
            }
        }

        $timeout();
    }

    $scope.modal = {};
    $scope.modal.data = {};
    
    $scope.modal.install = async () => {
        $scope.modal.data.install = {
            size: '',
            data: null,
        };
        $('#modal-install').modal('show');
    }

    $scope.modal.create = async () => {
        $scope.modal.data.create = {};
        $('#modal-create').modal('show');
    }

    $scope.event.install = async () => {
        try {
            let app_json = angular.copy(JSON.parse($scope.modal.data.install.data));
            if(app_json.info === undefined || app_json.route === undefined || app_json.apps === undefined) {
                toastr.error("Invalid data");
                return;
            }
            const { id } = app_json.info;
            let { code, data } = await API.install({
                id,
                data: JSON.stringify(app_json),
            });
            if(code !== 200) {
                toastr.error(data);
                return;
            }
            const { route } = app_json.info;
            const tmp = app_json.apps.filter(({name}) => {
                if(name.toLowerCase() === "readme") return true;
                return false;
            });
            if (tmp.length === 0) {
                location.reload();
                return;
            }
            const url = `/wiz/admin/${route}/readme`;
            console.log(url);
            window.open(url, "_blank");
            location.reload();
        }
        catch(err) {
            console.log(err);
        }
    }

    $scope.event.create = async () => {
        let pd = angular.copy($scope.modal.data.create);
        let res = await API.create(pd);

        if (res.code == 200) {
            location.reload();
        } else {
            toastr.error(res.data);
        }
    };


    $scope.event.change_id = async (val) => {
        $scope.modal.data.create.name = val;
        await API.timeout();
    };

    const install_file_handler = async (file) => {
        let size_kb = file.size / 1000;
        size_kb = +(Math.round(size_kb + "e+2")  + "e-2");
        $scope.modal.data.install.size = `${size_kb} KB`;
        $timeout();
        const fr = new FileReader();
        fr.readAsText(file, 'UTF-8');
        fr.addEventListener("load", (e) => {
            const { result } = e.target;
            $scope.modal.data.install.data = result;
            $timeout();
        });
    }

    const json_download = (filename, text) => {
        const element = document.createElement("a");
        element.setAttribute('href','data:text/plain;charset=utf-8, ' + encodeURIComponent(text));
        element.setAttribute('download', filename);
        document.body.appendChild(element);
        element.click();
    }

    $scope.event.download = async (plugin_id, plugin_name) => {
        const { code, data } = await API.download({
            id: plugin_id,
            name: plugin_name,
        });
        if(code !== 200) {
            toastr.error("FAILED");
            return;
        }

        const filename = plugin_name.replace(/\s+/g, "_") + ".wiz";
        json_download(filename, data);
    }

    document.querySelector("#plugin-install-input-file").addEventListener("change", (e) => {
        const files = e.target.files;
        if(files.length === 0) return;
        const file = files[0];
        try {
            if(file.name.split(".").slice(-1)[0].toLowerCase() !== "wiz") {
                toastr.error("Support Only 'wiz' ext");
                e.preventDefault();
                e.target.value = "";
                return;
            }
        }
        catch(err) {
            console.error(err);
            e.preventDefault();
            toastr.error("Support Only 'wiz' ext");
            e.target.value = "";
            return;
        }
        install_file_handler(file);
    });

    $scope.event.load();
}