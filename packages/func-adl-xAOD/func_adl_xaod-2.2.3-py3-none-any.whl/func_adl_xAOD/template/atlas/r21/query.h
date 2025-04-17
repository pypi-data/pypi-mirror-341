#ifndef analysis_query_H
#define analysis_query_H

#include <AnaAlgorithm/AnaAlgorithm.h>

{% for i in header_include_files %}
#include "{{i}}"
{% endfor %}


class query : public EL::AnaAlgorithm
{
public:
  // this is a standard algorithm constructor
  query (const std::string& name, ISvcLocator* pSvcLocator);

  // these are the functions inherited from Algorithm
  virtual StatusCode initialize () override;
  virtual StatusCode execute () override;
  virtual StatusCode finalize () override;

private:
  // Class level variables

  {% for l in class_decl %}
  {{l}}
  {% endfor %}

  {% for l in private_members %}
  {{l}}
  {% endfor %}
};

#endif