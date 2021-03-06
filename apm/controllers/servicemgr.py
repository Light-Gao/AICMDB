"""Author  Light Gao"""
from os import path
from flask import render_template, Blueprint, redirect, url_for
from apm.forms import AnsibleSvcInstanceForm
from apm.models import db, Service, Resource, SvcInstance
from apm.enums import globalenums
from apm.tasks.deploysvcinst import async_deploy_svc_inst
from flask import current_app

#Define svc_blueprint for Service Management
svc_blueprint = Blueprint('svc', __name__,
                          template_folder=path.join('../templates/service'),
                          url_prefix='/service')

#all route path will be added by '/service' as prefix automatically
@svc_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    current_app.logger.info('Show dashboard...')
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

@svc_blueprint.route('/error_page')
def show_error_page():
    return render_template('svc_error_page.html')

@svc_blueprint.route('/<int:service_id>/<int:service_type>/new_instance', methods=('GET', 'POST'))
def add_svc_instance(service_id, service_type):
    """function for adding service instance"""
    if not service_type:
        return redirect(url_for('svc.show_error_page'))
    svc_inst_form = AnsibleSvcInstanceForm()
    #if validate to submit, then active asynchronous task for service instance deploying backend
    if svc_inst_form.validate_on_submit():
        #create object for service instance
        new_svc_instance = SvcInstance(apm_svc_inst_name=svc_inst_form.name.data)
        new_svc_instance.apm_service_id = service_id
        new_svc_instance.status = globalenums.DEFAULT_STATUS_VALUE
        new_svc_instance.create_date = globalenums.DEFAULT_DATETIME
        new_svc_instance.apm_user_id = 1
        new_svc_instance.remark = svc_inst_form.remark.data

        #create asynchronous task and send it to task queue[celery_task_queue]
        task = async_deploy_svc_inst.delay(svc_type='Ansible',
                                           nodes=svc_inst_form.nodes.data,
                                           port=svc_inst_form.port.data)

        # add service instance object into database and commit
        if task:
            try:
                db.session.add(new_svc_instance)
                db.session.commit()
            except Exception:
                current_app.logger.error('An error occurred when creating service instance...')
                db.session.rollback()
                raise Exception

            return redirect(url_for('svc.show_svc_instance'))
        else:
            return redirect(url_for('svc.show_error_page'))

    svc = db.session.query(Service).get_or_404(service_id)
    attr = svc.attribute

    return render_template('svc_add_svcinstance.html',
                           svc=svc, attrs=attr, form=svc_inst_form)


