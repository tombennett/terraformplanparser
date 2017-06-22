import re

# I suck at python and this is a complete hack but it seems 
# to work for the job that I need it for

class TerraformResourceAttributePlan():
    # defines a change for an attribute on a terraform resource
    def __init__(self, attribute, old_value, new_value):
        self.attribute = attribute
        self.old_value = old_value
        self.new_value = new_value

class TerraformResourcePlan():
   # defines a plan for a specific terraform resource

   def __init__(self, resource_type, resource_name, change_type,  ):
       self.resource_type = resource_type
       self.resource_name = resource_name
       self.change_type = change_type
       self.attribute_plans = dict()

class TerraformPlan():
    # defines a plan for all terraform resources in the plan
    def __init__(self):
        self.resource_plans = list()

    def parse(self,plan):
        plan_regex = '(^\+ |^\- |^~ )(.*?^\n|.*)'
        plan_pattern = re.compile(plan_regex,re.DOTALL|re.MULTILINE)
        line_regex = '(^.*?)(?:[:])(.*)'
        line_pattern = re.compile(line_regex,re.MULTILINE)

        plan_matches = re.findall(plan_pattern,plan)

        for plan_match in plan_matches:
            action = plan_match[0].strip()
            tftext = plan_match[1]
            lines = tftext.splitlines()
            lines_len = len(lines)
            tfresource = lines[0].split('.')[0]
            tfresourcename = lines[0].split('.')[1]
            tfresourceplan = TerraformResourcePlan(tfresource,tfresourcename,action)

            # Now grab the attributes and their values
            line_matches = re.findall(line_pattern, tftext)

            for line_match in line_matches:
                attribute = line_match[0].strip()
                value = line_match[1].strip()
                # if value contains a => it means we have an old and a new value
                if '=>' in value:
                    old_value = value.split('=>')[0].strip()
                    new_value = value.split('=>')[1].strip()
                else:
                    old_value = ""
                    new_value = value
                
                tfattrplan = TerraformResourceAttributePlan(attribute,old_value,new_value)
                tfresourceplan.attribute_plans[attribute] = tfattrplan
            
            self.resource_plans.append(tfresourceplan)

#### Example pulling in a plan output from a saved file

f = open('plan.tfplan')
plan = f.read()
tfplan = TerraformPlan()
tfplan.parse(plan)
