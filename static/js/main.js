$(document).ready(function () {
    customScript.init({});
});
var self;
var customScript = {
    init: function (options) {
        this.settings = options;
        self = this;
        this.loginForm();
        this.logout();
        this.statisticalData();
    },
    loginForm: function () {
        $("#formLogin").validate({
            rules: {
                username: {
                    required: true
                },
                password: {
                    required: true
                }
            },
            messages: {
                username: "Username is required",
                password: "Password is required",
            },
            errorPlacement: function (error, element) {
                let frmgrp = element.parents(".form-group");
                error.appendTo(frmgrp);
            },
            submitHandler: function (form, e) {
                e.preventDefault();
                $.ajax({
                    type: $(form).attr('method'),
                    url: $(form).attr('action'),
                    data: $(form).serialize(),
                    dataType: 'json',
                    success: function (response) {
                        if (response.key) {
                            $.toast({
                                heading: 'Login',
                                text: 'Logged in successfully',
                                showHideTransition: 'fade',
                                bgColor: '#00FF00',
                                hideAfter: 10000,
                                textColor: '#000000',
                                position: 'top-right',
                            });
                            window.location.href = $(form).attr('data-success-url');
                        } else {
                            $.toast({
                                heading: 'Login',
                                text: response.error,
                                showHideTransition: 'fade',
                                allowToastClose: true,
                                bgColor: '#0CC5FB',
                                hideAfter: 10000,
                                textColor: '#000000',
                                position: 'top-right',
                            })
                        }
                    },
                    error: function (response) {
                        $.toast({
                            heading: 'Login',
                            text: response.responseJSON.error,
                            showHideTransition: 'fade',
                            allowToastClose: true,
                            bgColor: '#FB240C',
                            hideAfter: 10000,
                            textColor: '#000000',
                            position: 'top-right',
                        });
                    }
                });
                return false;
            }
        });
    },
    logout: function () {
        $("#logoutBtn").click(function () {
            var logout = $(this);
            $.ajax({
                type: 'POST',
                url: $(logout).attr('data-url'),
                dataType: 'json',
                success: function (response) {
                    if (response.detail) {
                        $.toast({
                            heading: 'Logout',
                            text: response.detail,
                            showHideTransition: 'fade',
                            allowToastClose: true,
                            bgColor: '#00FF00',
                            textColor: '#000000',
                            hideAfter: 10000,
                            position: 'top-right',
                        });
                        window.location.href = $(logout).attr('data-success-url');
                    } else {
                        $.toast({
                            heading: 'Logout',
                            text: response.error,
                            showHideTransition: 'fade',
                            allowToastClose: true,
                            bgColor: '#0CC5FB',
                            textColor: '#000000',
                            hideAfter: 10000,
                            position: 'top-right',
                        })
                    }
                },
                error: function (response) {
                    $.toast({
                        heading: 'Logout',
                        text: response.responseJSON.error,
                        showHideTransition: 'fade',
                        allowToastClose: true,
                        bgColor: '#FB240C',
                        textColor: '#000000',
                        hideAfter: 10000,
                        position: 'top-right',
                    });
                }
            });
            return false;
        })
    },
    getCookie: function (name) {
        if (!name) {
            return;
        }
        var cookieValue = null;

        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');

            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);

                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    },
    delete_cookie: function (name) {
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    },
    getDataPointsFormattedData: function (response) {
        let dataPoints = [];
        for (let i = 0; i < response.length; i++) {
            dataPoints.push({
                label: "Science",
                y: parseFloat(response[i].sci),
                legendText: "Science"
            }, {
                label: "Maths",
                y: parseFloat(response[i].math),
                legendText: "Maths"
            }, {
                label: "Language",
                y: parseFloat(response[i].language),
                legendText: "Language"
            }, {
                label: "Social",
                y: parseFloat(response[i].social),
                legendText: "Social"
            });
        }
        return dataPoints;
    },
    graphDataInit: function (divID, graphData) {
        $(divID).CanvasJSChart({
            title: {
                text: graphData.mainTitle,
                fontSize: 24
            },
            legend: {
                verticalAlign: "center",
                horizontalAlign: "right"
            },
            data: [
                {
                    type: "pie",
                    showInLegend: true,
                    toolTipContent: "{label} <br/> {y} %",
                    indexLabel: "{y} %",
                    dataPoints: graphData.dataPoints,
                }
            ]
        });
    },
    statisticalData: function () {
        $("#statisticalData").validate({
            rules: {
                data: {
                    required: true
                },
            },
            messages: {
                data: "This field is required",
            },
            errorPlacement: function (error, element) {
                let frmgrp = element.parents(".form-group");
                error.appendTo(frmgrp);
            },
            submitHandler: function (form, e) {
                const url = $(form).attr('action');
                let graphData = {};
                if (url.includes('class')) {
                } else if (url.includes('student')) {
                    graphData.mainTitle = 'Student Report for last five years';
                } else {
                    graphData.mainTitle = 'Report for year: ' + $(form).serialize().split("=")[1];
                }
                e.preventDefault();
                $.ajax({
                    type: $(form).attr('method'),
                    url: $(form).attr('action'),
                    data: $(form).serialize(),
                    dataType: 'json',
                    success: function (response) {
                        if (response || response.length) {
                            if (response.length || response) {
                                if (!url.includes('class')) {
                                    graphData.dataPoints = customScript.getDataPointsFormattedData(response);
                                    customScript.graphDataInit("#chartContainer", graphData)
                                } else {
                                    if (response.total_students.length > 0) {
                                        graphData.mainTitle = 'Total Student for last five years';
                                        graphData.dataPoints = customScript.getDataPointsFormattedData(response.total_students);
                                        customScript.graphDataInit("#totalStudentsChartContainer", graphData);
                                    }
                                    if (response.fail_students.length > 0) {
                                        graphData.mainTitle = 'Fail Student for last five years';
                                        graphData.dataPoints = customScript.getDataPointsFormattedData(response.fail_students);
                                        customScript.graphDataInit("#failStudentsChartContainer", graphData);
                                    }
                                    if (response.pass_students.length > 0) {
                                        debugger;
                                        graphData.mainTitle = 'Pass Student for last five years';
                                        graphData.dataPoints = customScript.getDataPointsFormattedData(response.pass_students);
                                        customScript.graphDataInit("#passStudentsChartContainer", graphData);
                                    }
                                }
                            }
                        }
                    },
                    error: function (response) {
                        $.toast({
                            title: 'Error',
                            content: "Something Went Wrong",
                            type: 'error',
                            delay: 5000
                        });
                    }
                });
                return false;
            }
        });
    },
};
