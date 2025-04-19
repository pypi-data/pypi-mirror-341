// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

// extra headers
{% for i in body_include_files %}
#include "{{i}}"
{% endfor %}


#include "TTree.h"

class Analyzer : public edm::EDAnalyzer
{
public:
   explicit Analyzer(const edm::ParameterSet &);
   ~Analyzer();

   static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
   virtual void beginJob();
   virtual void analyze(const edm::Event &, const edm::EventSetup &);
   virtual void endJob();

   virtual void beginRun(edm::Run const &, edm::EventSetup const &);
   virtual void endRun(edm::Run const &, edm::EventSetup const &);
   virtual void beginLuminosityBlock(edm::LuminosityBlock const &, edm::EventSetup const &);
   virtual void endLuminosityBlock(edm::LuminosityBlock const &, edm::EventSetup const &);
   
   TTree *myTree;

   {% for l in class_decl %}
   {{l}} 
   {% endfor %}
   
};

Analyzer::Analyzer(const edm::ParameterSet &iConfig)
{

   {% for l in book_code %}
   {{l}} 
   {% endfor %}

}

Analyzer::~Analyzer()
{

}

// ------------ method called for each event  ------------
void Analyzer::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup)
{
   using namespace edm;

#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example", pIn);
#endif

#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif

   {% for l in query_code %}
   {{l}} 
   {% endfor %}

}

// ------------ method called once each job just before starting event loop  ------------
void Analyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void Analyzer::endJob()
{
}

// ------------ method called when starting to processes a run  ------------
void Analyzer::beginRun(edm::Run const &, edm::EventSetup const &)
{
}

// ------------ method called when ending the processing of a run  ------------
void Analyzer::endRun(edm::Run const &, edm::EventSetup const &)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void Analyzer::beginLuminosityBlock(edm::LuminosityBlock const &, edm::EventSetup const &)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void Analyzer::endLuminosityBlock(edm::LuminosityBlock const &, edm::EventSetup const &)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void Analyzer::fillDescriptions(edm::ConfigurationDescriptions &descriptions)
{
   edm::ParameterSetDescription desc;
   desc.setUnknown();
   descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(Analyzer);
