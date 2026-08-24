class SkillConductor < Formula
  desc "Cross-host Skill engineering toolkit and plugin for all AI agents"
  homepage "https://github.com/imMamdouhaboammar/skill-conductor"
  url "https://github.com/imMamdouhaboammar/skill-conductor/archive/refs/tags/v4.0.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000" # Updated automatically in release workflow
  license "MIT"
  head "https://github.com/imMamdouhaboammar/skill-conductor.git", branch: "main"

  depends_on "python@3.12" => :optional

  def install
    # Install libexec payload
    libexec.install Dir["*"]

    # Create binary wrapper
    bin.install_symlink libexec/"bin/skill-conductor"
  end

  def caveats
    <<~EOS
      Skill Conductor has been installed!

      To check your environment and detected agent hosts:
        skill-conductor doctor

      To install the skills suite to all detected agents:
        skill-conductor install --agent all

      To explore the skills catalog:
        skill-conductor list
    EOS
  end

  test do
    assert_match "skill-conductor", shell_output("#{bin}/skill-conductor --version")
    assert_match "Skill Conductor Doctor", shell_output("#{bin}/skill-conductor doctor")
  end
end
