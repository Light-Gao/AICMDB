"""Author  Light Gao
Mailto  gaoliang@asiainfo.com
Date    20180112
Last Modified 20180228"""
from os import path
from flask import render_template, Blueprint, redirect, url_for
from apm.forms import SvcInstanceForm
from apm.models import db, Service, Resource, SvcInstance
from apm.enums import globalenums

#Define svc_blueprint for Service Management
svc_blueprint = Blueprint('svc', __name__,
                          template_folder=path.join('../templates/service'),
                          url_prefix='/service')

@svc_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@svc_blueprint.route('/')
def show_svc():
    #view function for service
    svc = db.session.query(Service).all()
    return render_template('svc_service.html', service=svc)

@svc_blueprint.route('/resource')
def show_resource():
    res = db.session.query(Resource).filter_by(status='1').all()
    return render_template('svc_resource.html', resource=res)

@svc_blueprint.route('/instance', methods=('GET', 'POST'))
def show_svc_instance():
    svc_inst = db.session.query(SvcInstance).all()
    return render_template('svc_svcinstance.html', svc_instance=svc_inst)

@svc_blueprint.route('/<int:service_id>/new_instance', methods=('GET', 'POST'))
def add_svc_instance(service_id):
    """function for adding service instance"""
    svc_inst_form = SvcInstanceForm()
    if svc_inst_form.validate_on_submit():
        new_svc_instance = SvcInstance(apm_svc_inst_name=svc_inst_form.name.data)
        new_svc_instance.apm_service_id = service_id
        new_svc_instance.status = globalenums.DEFAULT_STATUS_VALUE
        new_svc_instance.create_date = globalenums.DEFAULT_DATETIME
        new_svc_instance.apm_user_id = 1
        new_svc_instance.remark = svc_inst_form.remark.data
        db.session.add(new_svc_instance)
        db.session.commit()
        return redirect(url_for('svc.show_svc_instance'))

    svc = db.session.query(Service).get_or_404(service_id)

    return render_template('svc_add_svcinstance.html', svc=svc, form=svc_inst_form)


