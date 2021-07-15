	# -*- coding: utf-8 -*-



from dateutil import relativedelta
from datetime import timedelta
from functools import partial
import datetime

from odoo import api, exceptions, fields, models, _
from odoo.exceptions import ValidationError
from odoo.addons.resource.models.resource import make_aware, Intervals
from odoo.tools.float_utils import float_compare
from odoo.exceptions import AccessError, UserError
from odoo import api, fields, models, _
import pytz 
import pdb
class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    resource_id=fields.Many2one('resource.group','Resource')
    # employee_line_ids = fields.Many2many('hr.employee', 'mrp_r_w_id','emp_id',string="Employees")

    # shift_name = fields.Char("Name",copy=False)
    # start_date = fields.Datetime(string='Start Date', index=True,  copy=False, default=fields.Datetime.now)
    # end_date = fields.Datetime(string='End Date', index=True,  copy=False)

    # @api.constrains('start_date')
    # def _code_constrains(self):
    #     if self.start_date > self.end_date:
    #         raise ValidationError(_("'Start Date' must be before 'End Date'"))
    # @api.onchange('workcenter_id')
    # def get_shit_time(self):
    #     self.shift_id = self.workcenter_id.resource_calendar_id.id
   

  
class MrpProductionShift(models.Model):
    _inherit = 'mrp.production'

    def _create_workorder(self):
        res = super(MrpProductionShift,self)._create_workorder()
        if self.workorder_ids:
            for each in self.workorder_ids:
                each.shif_calendar_id= each.workcenter_id.resource_calendar_id.id
                each.resource_id= each.operation_id.resource_id.id
               
                each.employee_ids=  [(6, 0, each.operation_id.resource_id.employee_line_ids.ids)] 

    def write(self, vals):
        res = super(MrpProductionShift, self).write(vals)
        for each_order in self.workorder_ids:
            if each_order.date_planned_start and each_order.date_planned_finished:

                start_day =each_order.date_planned_start.weekday()
                end_day =each_order.date_planned_finished.weekday()

                attendance=self.env['resource.calendar.attendance']
                leave_obj=self.env['hr.leave']
                attendance_ids = attendance.search([('calendar_id','=',each_order.shif_calendar_id.id),('dayofweek','=',each_order.date_planned_start.weekday())])
                # Converting the time zones to compare the times
                old_tz = pytz.timezone('UTC')
                new_tz = pytz.timezone('Asia/Calcutta')
                new_date = old_tz.localize(each_order.date_planned_start).astimezone(new_tz)
                new_date_to = old_tz.localize(each_order.date_planned_finished).astimezone(new_tz)
                
                # finding the employees leaves
                # 
                for each_emp in each_order.employee_ids.ids:
                    if each_emp:
                        
                        leaves_ids = leave_obj.search([('id','=',each_emp),('date_from','>=',each_order.date_planned_start),('date_to','<=',each_order.date_planned_finished)])
                        # leaves_ids = leave_obj.search([('id','=',each_emp),('date_from','<=',self.date_planned_start)])
                        # leaves_ids = leave_obj.search([('id','=',each_emp)])
                        # leaves_ids = leave_obj.search([('state','=','validate1'),])
                        if leaves_ids:

                            raise UserError(_('%s is in leave', each_emp.name))

                # for each in self.self.workcenter_id.
                # checking the with resource dates in the routings dates
                if attendance_ids:
                    match = False
                    for each_line in attendance_ids:
                        if  each_line.hour_from <= new_date.hour and each_line.hour_from <= new_date_to.hour and each_line.hour_to <= new_date.hour and each_line.hour_to <= new_date_to.hour:
                            match = True
                            break
                    if not match:
                        raise UserError(' Planning time is beyond the Shift Time')
        return res
# class MrpWorkcenterShift(models.Model):
#     _inherit = 'mrp.workcenter'

    

   
class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'


    resource_id= fields.Many2one('resource.group',string='Resource')
    # routing_id = fields.Many2one('mrp.routing.workcenter',string='Routing',domain=[('is_master','=',True)])
    resource_name= fields.Char("Resource Group")
    employee= fields.Char("Employee",compute='get_employee_names',store=True)
    employee_ids = fields.Many2many('hr.employee',string='Employees')
    shif_calendar_id = fields.Many2one('resource.calendar',string='Shift')
    is_shift_change= fields.Boolean('Use Shift')


    @api.onchange('date_planned_start', 'duration_expected')
    def _onchange_date_planned_start(self):
        res = super(MrpWorkorder, self)._onchange_date_planned_start()
        if not self.is_shift_change:
            if self.date_planned_start and self.duration_expected:
                self.date_planned_finished = self.workcenter_id.resource_calendar_id.plan_hours(
                    self.duration_expected / 60.0, self.date_planned_start,
                    compute_leaves=True, domain=[('time_type', 'in', ['leave', 'other'])]
                )
        else:
            if self.date_planned_start and self.duration_expected:
                self.date_planned_finished = self.shif_calendar_id.plan_hours(
                    self.duration_expected / 60.0, self.date_planned_start,
                    compute_leaves=True, domain=[('time_type', 'in', ['leave', 'other'])])



    def _get_first_available_shift(self, start_datetime, duration):
        # pdb.set_trace()
        """Get the first available interval for the workcenter in `self`.

        The available interval is disjoinct with all other workorders planned on this workcenter, but
        can overlap the time-off of the related calendar (inverse of the working hours).
        Return the first available interval (start datetime, end datetime) or,
        if there is none before 700 days, a tuple error (False, 'error message').

        :param start_datetime: begin the search at this datetime
        :param duration: minutes needed to make the workorder (float)
        :rtype: tuple
        """

        self.ensure_one()
        # pdb.set_trace()
        # self.env['mrp.workorder'].search([('workcenter_id','=',self.id)])
        start_datetime, revert = make_aware(start_datetime)

        get_available_intervals = partial(self.shif_calendar_id._work_intervals, domain=[('time_type', 'in', ['other', 'leave'])], resource=self.shif_calendar_id)
        get_workorder_intervals = partial(self.shif_calendar_id._leave_intervals, domain=[('time_type', '=', 'other')], resource=self.shif_calendar_id)

        remaining = duration
        start_interval = start_datetime
        delta = timedelta(days=14)

        for n in range(50):  # 50 * 14 = 700 days in advance (hardcoded)
            dt = start_datetime + delta * n
            available_intervals = get_available_intervals(dt, dt + delta)
            workorder_intervals = get_workorder_intervals(dt, dt + delta)
            for start, stop, dummy in available_intervals:
                interval_minutes = (stop - start).total_seconds() / 60
                # If the remaining minutes has never decrease update start_interval
                if remaining == duration:
                    start_interval = start
                # If there is a overlap between the possible available interval and a others WO
                if Intervals([(start_interval, start + timedelta(minutes=min(remaining, interval_minutes)), dummy)]) & workorder_intervals:
                    remaining = duration
                    start_interval = start
                elif float_compare(interval_minutes, remaining, precision_digits=3) >= 0:
                    return revert(start_interval), revert(start + timedelta(minutes=remaining))
                # Decrease a part of the remaining duration
                remaining -= interval_minutes
        return False, 'Not available slot 700 days after the planned start'

    # date_planned_start = fields.Datetime(
    #     'Scheduled Start Date',
    #     compute='_compute_dates_planned_shift',
    #     inverse='_set_dates_planned',
    #     states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
    #     store=True, copy=False)
    # date_planned_finished = fields.Datetime(
    #     'Scheduled End Date',
    #     compute='_compute_dates_planned_shift',
    #     inverse='_set_dates_planned',
    #     states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
    #     store=True, copy=False)


    # @api.depends('shif_calendar_id')
    # def _compute_dates_planned_shift(self):
    #     for workorder in self:
    #         workorder.date_planned_start = workorder.shif_calendar_id.date_from
    #         workorder.date_planned_finished = workorder.shif_calendar_id.date_to

    @api.onchange('shif_calendar_id')
    def get_date(self):
        print("selfffffffffffffffffffffff",self)
        for workorder in self:
            workcenters = workorder.workcenter_id | workorder.workcenter_id.alternative_workcenter_ids
            if workcenters:
                best_finished_date = datetime.datetime.max
                vals = {}
                start_date = max(workorder.production_id.date_planned_start, datetime.datetime.now())
                for workcenter in workcenters:
                    # compute theoretical duration
                    if workorder.workcenter_id == workcenter:
                        duration_expected = workorder.duration_expected
                    else:
                        duration_expected = workorder._get_duration_expected(alternative_workcenter=workcenter)

                    # start_datetime, revert = make_aware(start_date)

                    # get_available_intervals = partial(self.shif_calendar_id._work_intervals, domain=[('time_type', 'in', ['other', 'leave'])], resource=self.resource_id)
                    # get_workorder_intervals = partial(self.shif_calendar_id._leave_intervals, domain=[('time_type', '=', 'other')], resource=self.resource_id)

                    # remaining = duration_expected
                    # start_interval = start_datetime
                    # delta = timedelta(days=14)

                    # for n in range(50):  # 50 * 14 = 700 days in advance (hardcoded)
                    #     dt = start_datetime + delta * n
                    #     available_intervals = get_available_intervals(dt, dt + delta)
                    #     workorder_intervals = get_workorder_intervals(dt, dt + delta)
                    #     for start, stop, dummy in available_intervals:
                    #         interval_minutes = (stop - start).total_seconds() / 60
                    #         # If the remaining minutes has never decrease update start_interval
                    #         if remaining == duration:
                    #             start_interval = start
                    #         # If there is a overlap between the possible available interval and a others WO
                    #         if Intervals([(start_interval, start + timedelta(minutes=min(remaining, interval_minutes)), dummy)]) & workorder_intervals:
                    #             remaining = duration
                    #             start_interval = start
                    #         elif float_compare(interval_minutes, remaining, precision_digits=3) >= 0:
                    #             return revert(start_interval), revert(start + timedelta(minutes=remaining))
                    #         # Decrease a part of the remaining duration
                    #         remaining -= interval_minutes
                    # pdb.set_trace()
                    from_date, to_date = self._get_first_available_shift(start_date, duration_expected)
                    # If the workcenter is unavailable, try planning on the next one
                    if not from_date:
                        continue
                    # Check if this workcenter is better than the previous ones
                    if to_date and to_date < best_finished_date:
                        best_start_date = from_date
                        best_finished_date = to_date
                        best_workcenter = workcenter
                        vals = {
                            'workcenter_id': workcenter.id,
                            'duration_expected': duration_expected,
                            'is_shift_change': True,
                        }

                # If none of the workcenter are available, raise
                if best_finished_date == datetime.datetime.max:
                    raise UserError(_('Impossible to plan the workorder. Please check the workcenter availabilities.'))

                # Instantiate start_date for the next workorder planning
                if workorder.next_work_order_id:
                    start_date = best_finished_date

                # Create leave on chosen workcenter calendar
                leave = self.env['resource.calendar.leaves'].create({
                    'name': workorder.display_name,
                    'calendar_id': best_workcenter.resource_calendar_id.id,
                    'date_from': best_start_date,
                    'date_to': best_finished_date,
                    'resource_id': best_workcenter.resource_id.id,
                    'time_type': 'other'
                })
                vals['leave_id'] = leave.id
                workorder.write(vals)
                workorder.write(vals)

                
            # self.with_context(force_date=True).write({
            #     'date_planned_start': self.workorder_ids[0].date_planned_start,
            #     'date_planned_finished': self.workorder_ids[-1].date_planned_finished
            # })
        
        
    @api.onchange("resource_id")
    def get_resource_date(self):
        if self.resource_id:
            workcenter_ids = self.env['mrp.workorder'].search([('resource_id','=',self.resource_id.id)])
            resource_is_in_used= workcenter_ids.filtered(lambda m: m.state == 'progress')
            if resource_is_in_used:
                raise UserError (_("%s resource group is in inprogress",self.resource_id.name))
            self.employee_ids = [(6, 0, self.resource_id.employee_line_ids.ids)]
            self.resource_name = self.resource_id.name

    @api.depends('employee_ids')
    def get_employee_names(self):
        new_names=''
        for each in self.employee_ids:
            if each:
                new_names = new_names +' '+each.name
            if len(new_names)>1:
                self.employee = new_names
            else:
                self.employee = False


class ResourceGroup(models.Model):
    _name = 'resource.group'
    _description = 'resource.group'


    name=fields.Char('Name')
    start_date = fields.Datetime(string='Start Date', index=True,  copy=False, default=fields.Datetime.now)
    end_date = fields.Datetime(string='End Date', index=True,  copy=False)
    employee_line_ids = fields.Many2many('hr.employee', 'resource_id','emp_id',string="Employees")

    # @api.constrains('start_date')
    # def _code_constrains(self):
    #     if self.start_date > self.end_date:
    #         raise ValidationError(_("'Start Date' must be before 'End Date'"))






